import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 115200)

def geiger_loop(q_geiger_out):
    while True:
        resultado = str(ser.readline().decode("ascii")).split(',')
        try:
          cpm = str(resultado[0])
          svh = str(resultado[1])
          msvh = str(resultado[2])
          dust = str(resultado[3]).strip() # eliminar newline char
        except:
          cpm = "0"
          svh = "0"
          msvh = "0"
          dust = "0"
        q_geiger_out.put("d" + cpm)
        q_geiger_out.put("e" + svh)
        q_geiger_out.put("f" + msvh)
        q_geiger_out.put("g" + dust)
        sleep(5)