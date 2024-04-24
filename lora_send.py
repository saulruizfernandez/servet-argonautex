from SX127x.LoRa import *
from SX127x.board_config import BOARD

from time import sleep

cadena = ""

# Derived class from LoRa (pyLoRa)
class MyLoRa(LoRa):

  def __init__(self, verbose=False):
    super(MyLoRa, self).__init__(verbose)
    self.set_mode(MODE.SLEEP)
    self.set_dio_mapping([1,0,0,0,0,0])

  def start(self, q_lora_in):
    self.set_mode(MODE.TX)
    while True:
      try:
        cadena = q_bme_in.get(block=False)
      except:
        pass
      sleep(1)

  def on_tx_done(self):
    self.set_mode(MODE.STDBY)
    self.clear_irq_flags(TxDone=1)
    sleep(5) # Sent every 5 seconds
    self.write_payload(list(cadena.encode('ascii')))
    print("paquete enviado")
    self.set_mode(MODE.TX)

def LoraSend(q_lora_in):
  BOARD.setup()
  lora = MyLoRa(verbose=False)
  lora.set_pa_config(pa_select=1)
  lora.set_freq(411.5)
  try:
    lora.start(q_lora_in)
  except:
    pass
  finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
