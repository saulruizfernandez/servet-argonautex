#!/usr/bin/python
from multiprocessing import Queue
from queue import Empty as QueueEmpty
from threading import Thread

from time import sleep

from bme_main import bme_loop
from gps_main import gps_loop
from geiger_main import geiger_loop
from lora_send import LoraSend

# Write header in CSV
fichero_datos = open('../datos/datos_servet.csv', 'a')
fichero_datos.write('temperatura,humedad,presion,latitud,longitud,altitud,cpm,nsvh,usvh,ugmmm\n')
fichero_datos.close()

def unified_loop(q_bme_in, q_gps_in, q_geiger_in, q_lora_out):
  temperatura = 0
  humedad = 0
  presion = 0
  latitud = 0
  longitud = 0
  altitud = 0
  cpm = 0
  svh = 0
  msvh = 0
  dust = 0

  while True:
    sleep(5)
    chain = ''
    # BME
    for i in range (3):
      try:
        data_bme = q_bme_in.get(block=False)
        if (data_bme[0] == "t"):
          temperatura = data_bme[1:]
        elif (data_bme[0] == "h"):
          humedad = data_bme[1:]
        elif (data_bme[0] == "p"):
          presion = data_bme[1:]
      except QueueEmpty:
        pass
    chain = f'{temperatura},{humedad},{presion},'

    # GPS
    for i in range (3):
      try:
        data_gps = q_gps_in.get(block=False)
        if (data_gps[0] == "a"):
          latitud = data_gps[1:]
        elif (data_gps[0] == "b"):
          longitud = data_gps[1:]
        elif (data_gps[0] == "c"):
          altitud = data_gps[1:]
      except QueueEmpty:
        pass
    chain += f'{latitud},{longitud},{altitud},'

    # GEIGER and DUST
    for i in range (3):
      try:
        data_geiger = q_geiger_in.get(block=False)
        if (data_geiger[0] == "d"):
          cpm = data_geiger[1:]
        elif (data_geiger[0] == "e"):
          svh = data_geiger[1:]
        elif (data_geiger[0] == "f"):
          msvh = data_geiger[1:]
        elif (data_geiger[0] == "g"):
          dust = data_geiger[1:]
      except QueueEmpty:
        pass

    chain += f'{cpm},{svh},{msvh},{dust}'
    # Save data to CSV
    fichero_datos = open('../datos/datos_servet.csv', 'a')
    fichero_datos.write(chain + '\n')
    fichero_datos.close()
    # Send data over LoRa
    q_lora_out.put(chain)

# Shared queues
q_bme = Queue()
q_gps = Queue()
q_geiger = Queue()
q_lora = Queue()

# Threads
thread_bme = Thread(target=bme_loop, args=(q_bme, ))
thread_gps = Thread(target=gps_loop, args=(q_gps, ))
thread_geiger = Thread(target=geiger_loop, args=(q_geiger, ))
thread_lora = Thread(target=LoraSend, args=(q_lora, ))
thread_unif = Thread(target=unified_loop, args=(q_bme, q_gps, q_geiger, q_lora, ))

try:
  thread_bme.start()
  thread_gps.start()
  thread_geiger.start()
  thread_lora.start()
  thread_unif.start()
except:
  pass
finally:
  pass