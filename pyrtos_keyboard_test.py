from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys
import pyRTOS
import qwiic_scmd
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import keyboard
import os
# import threading

os.system("stty -echo")
R_MTR = 0
L_MTR = 1
FWD = 0
BWD = 1
speed=250
key=''
def func_keydown(event):
    global key
#     print('key down')
#     print(event.name)
    key=event.name+" pressed"
def func_keyup(event):
    global key
#     print('key down')
#     print(event.name)
    key=event.name+" released"
keyboard.on_press_key("up",func_keydown,True)
keyboard.on_release_key("up",func_keyup,True)
keyboard.on_press_key("down",func_keydown,True)
keyboard.on_release_key("down",func_keyup,True)
keyboard.on_press_key("left",func_keydown,True)
keyboard.on_release_key("left",func_keyup,True)
keyboard.on_press_key("right",func_keydown,True)
keyboard.on_release_key("right",func_keyup,True)

myMotor = qwiic_scmd.QwiicScmd()
if myMotor.connected == False:
    print("Motor Driver not connected. Check connections.", file=sys.stderr)
    sys.exit(0)
myMotor.begin()
print("Motor initialized.")
time.sleep(.250)
myMotor.set_drive(0,0,0)
myMotor.set_drive(1,0,0)
myMotor.enable()
print("Motor enabled")
time.sleep(.250)
    

def task1(self):
    global myEncoders
    global myMotor
    global ENC1
    global ENC2
    global key
    
    SAMPLETIME = 0.1
    
    yield
    
    while True:
        if key=="up pressed":
            print(key)
            myMotor.set_drive(L_MTR,FWD,speed)
            myMotor.set_drive(R_MTR,FWD,speed)
        if key=="up released":
            myMotor.set_drive(0,0,0)
            myMotor.set_drive(1,0,0)
        if key=="down pressed":
            myMotor.set_drive(L_MTR,BWD,speed)
            myMotor.set_drive(R_MTR,BWD,speed)
        if key=="down released":
            myMotor.set_drive(0,0,0)
            myMotor.set_drive(1,0,0)
        if key=="left pressed":
            myMotor.set_drive(L_MTR,FWD,speed/2)
            myMotor.set_drive(R_MTR,BWD,speed/2)
        if key=="left released":
            myMotor.set_drive(0,0,0)
            myMotor.set_drive(1,0,0)
        if key=="right pressed":
            myMotor.set_drive(L_MTR,BWD,speed/2)
            myMotor.set_drive(R_MTR,FWD,speed/2)
        if key=="right released":
            myMotor.set_drive(0,0,0)
            myMotor.set_drive(1,0,0)

        yield [pyRTOS.timeout(SAMPLETIME)]

       
def task3(self):
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
# pyRTOS.add_task(pyRTOS.Task(task2))
# pyRTOS.add_task(pyRTOS.Task(task3))

try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    print("Ending example.")
    myMotor.disable()
    os.system("stty echo")
    print ("\n")
    sys.exit(0)




