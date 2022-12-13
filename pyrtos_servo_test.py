import pyRTOS
import keyboard
import os
import pi_servo_hat
import time

os.system("stty -echo")
servo = pi_servo_hat.PiServoHat()
servo.restart()
servo.move_servo_position(0, 90)
time.sleep(1)
servo.move_servo_position(1, 90)
time.sleep(1)
pos_v=90
pos_h=90
# Restart Servo Hat (in case Hat is frozen/locked)


key=''
def func_keydown(event):
    global key

    if event.scan_code==115:
        key="sup pressed"
    if event.scan_code==114:
        key="sdown pressed"
    if event.scan_code==165:
        key="sleft pressed"
    if event.scan_code==163:
        key="sright pressed"
    if event.scan_code==164:
        key="scentral pressed"        
def func_keyup(event):
    global key

    if event.scan_code==115:
        key="sup released"
    if event.scan_code==114:
        key="sdown released"    
    if event.scan_code==165:
        key="sleft released"
    if event.scan_code==163:
        key="sright released"
    if event.scan_code==164:
        key="scentral released"
        
keyboard.on_press_key(115,func_keydown,True)
keyboard.on_release_key(115,func_keyup,True)
keyboard.on_press_key(114,func_keydown,True)
keyboard.on_release_key(114,func_keyup,True)
keyboard.on_press_key(165,func_keydown,True)
keyboard.on_release_key(165,func_keyup,True)
keyboard.on_press_key(163,func_keydown,True)
keyboard.on_release_key(163,func_keyup,True)
keyboard.on_release_key(164,func_keydown,True)
keyboard.on_release_key(164,func_keyup,True)
# keyboard.on_release(func_keyup)
def task1(self):
#     ledpin1 = machine.Pin(0, machine.Pin.OUT)
#     ledpin1.value(0)
    global key
    global servo
    global pos_v
    global pos_h
    
    yield
    
    while True:
        if key=="sup pressed":
            print(pos_v)
            
            if pos_v>30:
                pos_v=pos_v-1
            
            servo.move_servo_position(1, pos_v)
        if key=="sdown pressed":
            print(pos_v)
            
            if pos_v<120:
                pos_v=pos_v+1
            
            servo.move_servo_position(1, pos_v)
        if key=="sright pressed":
            print(pos_h)
            
            if pos_h>30:
                pos_h=pos_h-1
            
            servo.move_servo_position(0, pos_h)
        if key=="sleft pressed":
            print(pos_h)
            
            if pos_h<120:
                pos_h=pos_h+1
            
            servo.move_servo_position(0, pos_h)
        if key=="scentral pressed":
            print("center")
                  
            servo.move_servo_position(0, 90)
            servo.move_servo_position(1, 90)
            pos_v=90
            pos_h=90
        yield [pyRTOS.timeout(0.1)]

def task2(self):
#     ledpin2 = machine.Pin(1, machine.Pin.OUT)
#     ledpin2.value(0)
    global key
    yield
    
    while True:
        if key:
            print(key)
#             key=''
#         print("task2 ",a)
#         print("task2")
        yield [pyRTOS.timeout(0.1)]
    
pyRTOS.add_task(pyRTOS.Task(task1))
pyRTOS.add_task(pyRTOS.Task(task2))

try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    os.system("stty echo")
    print ("\n")
    sys.exit(0)
