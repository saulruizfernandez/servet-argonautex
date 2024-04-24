# Takes a picture every second and saves it to /home/images/image<id>.jpg

import subprocess

i = 0
try:
  i = subprocess.check_output('ls -t /home/servet/images | head -n1 | grep -o "0"', shell=True, text=True)
  i = int(i)
except:
  print("No se ha encontrado la imagen")
    

from picamera import PiCamera
from time import sleep

camera = PiCamera()
sleep(2) # Espera a que la ganancia automatica se ajuste
camera.set_awb_mode = 'fluorescent'

while True:
    i += 1
    camera.capture('/home/servet/images/image%s.jpg' % i)
    sleep(10)
