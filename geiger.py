import time
from raspberry import Board, Pin

btn = Pin(Pin.P23, Pin.IN)

time_gap = 0
start_time = 0
count = 0
time_gap = 5
uSvh = 0
 
def zero():
    global start_time,count
    start_time = time.time()
    count = 0
 
def btn_falling_handler(pin):
    global count
    count += 1
 
zero()
btn.irq(trigger=Pin.IRQ_FALLING, handler=btn_falling_handler) 
 
def get_cpm():
    global uSvh
    if time.time() - start_time >= time_gap: 
        uSvh = round((count/151)*(60/time_gap),2)
        print("uSvh=",uSvh)
        zero()
