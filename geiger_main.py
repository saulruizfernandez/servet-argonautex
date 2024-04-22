import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 115200)

def geiger_loop(q_geiger_out):
    while True:
        resultado = str(ser.readline().decode("ascii")).split(',')
        q_geiger_out.put("d" + str(resultado[0]))
        q_geiger_out.put("e" + str(resultado[1]))
        q_geiger_out.put("f" + str(resultado[2]))
        sleep(1)