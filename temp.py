from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys
import pyRTOS
import qwiic_scmd
import subprocess
# import digitalio
# import board
# from PIL import Image, ImageDraw, ImageFont
# from adafruit_rgb_display import st7789
# import keyboard
# import os
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
# import threading

# os.system("stty -echo")
R_MTR = 0
L_MTR = 1
FWD = 0
BWD = 1
speed=250
tspeed=180
key=''

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

def print_add(joy):
    print('Added', joy)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    print('Key:', key)
    if key=="Hat 0 [Up]":
        print("UP")
        myMotor.set_drive(L_MTR,FWD,speed)
        myMotor.set_drive(R_MTR,FWD,speed)
    if key=="Hat 0 [Centered]":
        print("STOP")
        myMotor.set_drive(0,0,0)
        myMotor.set_drive(1,0,0)
    if key=="Hat 0 [Down]":
        print("DOWN")
        myMotor.set_drive(L_MTR,BWD,speed)
        myMotor.set_drive(R_MTR,BWD,speed)
    if key=="Hat 0 [Left]":
        print("LEFT")
        myMotor.set_drive(L_MTR,FWD,tspeed)
        myMotor.set_drive(R_MTR,BWD,tspeed)
    if key=="Hat 0 [Right]":
        print("RIGHT")
        myMotor.set_drive(L_MTR,BWD,tspeed)
        myMotor.set_drive(R_MTR,FWD,tspeed)
run_event_loop(print_add, print_remove, key_received)
print("After event loop")
