from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

from time import sleep

BOARD.setup()
parser = LoRaArgumentParser("A simple LoRa beacon")
parser.add_argument('--single', '-S', dest='single', default=False, action="store_true", help="Single transmission")
parser.add_argument('--wait', '-w', dest='wait', default=1, action="store", type=float, help="Waiting time between transmissions (default is 0s)")

# Derived class from LoRa (pyLoRa)
class MyLoRa(LoRa):

  def __init__(self, verbose=False):
    super(MyLoRa, self).__init__(verbose)
    self.set_mode(MODE.SLEEP)
    self.set_dio_mapping([1,0,0,0,0,0])

  def start(self):
    self.set_mode(MODE.TX)
    while True:
      sleep(1)

  def on_tx_done(self):
    self.set_mode(MODE.STDBY)
    self.clear_irq_flags(TxDone=1)
    sleep(5) # Sent every 5 seconds
    self.write_payload(list("hello".encode('ascii')))
    #print("paquete enviado")
    self.set_mode(MODE.TX)

lora = MyLoRa(verbose=False)
lora.set_pa_config(pa_select=1)
lora.set_freq(411.5)
try:
  lora.start()
except:
  pass
finally:
  lora.set_mode(MODE.SLEEP)
  BOARD.teardown()
