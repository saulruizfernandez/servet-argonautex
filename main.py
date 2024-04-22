#!/usr/bin/python
from multiprocessing import Queue
from queue import Empty as QueueEmpty
from threading import Thread
from time import sleep
from bme_main import bme_loop
from gps_main import gps_loop

def unified_loop(q_bme_in, q_gps_in):
  while True:
    chain = ''
    # BME
    try:
      data_bme = q_bme_in.get(block=False)
      if (data_bme[0] == "t"):
        temperatura = data_bme[1:]
      elif (data_bme[0] == "h"):
        humedad = data_bme[1:]
      elif (data_bme[0] == "p"):
        presion = data_bme[1:]
    except QueueEmpty:
      temperatura = 0
      humedad = 0
      presion = 0
    chain = f'{temperatura},{humedad},{presion},'

    # GPS
    try:
      data_gps = q_gps_in.get(block=False)
      if (data_gps[0] == "a"):
        latitud = data_gps[1:]
      elif (data_gps[0] == "b"):
        longitud = data_gps[1:]
      elif (data_gps[0] == "c"):
        altitud = data_gps[1:]
    except QueueEmpty:
      latitud = 0
      longitud = 0
      altitud = 0
    chain += f'{latitud},{longitud},{altitud}'
    
    # Print the chain
    print(chain)
    sleep(1)

# Shared queues
q_bme = Queue(maxsize=30)
q_gps = Queue(maxsize=30)

# Threads
thread_bme = Thread(target=bme_loop, args=(q_bme, ))
thread_gps = Thread(target=gps_loop, args=(q_gps, ))
thread_unif = Thread(target=unified_loop, args=(q_bme, q_gps, ))

thread_bme.start()
thread_gps.start()
thread_unif.start()