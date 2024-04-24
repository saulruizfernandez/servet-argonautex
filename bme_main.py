# Temperature, humidity and pressure values, provided by bme680 sensor

from adafruit_bme680 import Adafruit_BME680_I2C
from board import I2C
from time import sleep

i2c = I2C()
bme680 = Adafruit_BME680_I2C(i2c, debug=False)
TEMPERATURE_OFFSET = -5  # Temperature correction

"""
Function sending bme data. Inserts in the queue the temperature, humidity and pressure values
"""
def bme_loop(q_bme_out):
    while True:
        q_bme_out.put("t" + str(round(bme680.temperature + TEMPERATURE_OFFSET, 2)))
        q_bme_out.put("h" + str(round(bme680.relative_humidity, 2)))
        q_bme_out.put("p" + str(round(bme680.pressure, 2)))
        sleep(5)
