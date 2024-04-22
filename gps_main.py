import time
import board
import busio
import adafruit_gps
import serial

uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)

# Creamos una instancia del GPS
gps = adafruit_gps.GPS(uart, debug=False)

# GGA y RMC (información requerida)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Frecuencia de actualización (1hz)
gps.send_command(b"PMTK220,1000")

# Main loop runs forever printing the location, etc. every second.
def gps_loop(q_gps_out):
  last_print = time.monotonic()
  while True:
    gps.update()
    current = time.monotonic()
    # Una vez por segundo, si hay fix, se envían los datos
    if ((current - last_print) >= 1.0):
        last_print = current
        if not gps.has_fix:
            # Si no hay fix vuelve a intentarlo
            continue
         # "a" latitud, "b" longitud, "c" altitud
        q_gps_out.put("a" + str("{0:.6f}".format(gps.latitude)))
        q_gps_out.put("b" + str("{0:.6f}".format(gps.longitude)))
        q_gps_out.put("c" + str(round(gps.altitude_m, 2)))