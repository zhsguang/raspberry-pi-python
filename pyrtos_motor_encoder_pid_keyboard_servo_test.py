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
import pi_servo_hat
# import threading

os.system("stty -echo")
servo = pi_servo_hat.PiServoHat()
servo.restart()
pos_v=130
pos_h=40
servo.move_servo_position(0, pos_h)
time.sleep(1)
servo.move_servo_position(1, pos_v)
time.sleep(1)
key=''
key_last=''
def func_keydown(event):
    global key
#     print('key down')
    if event.scan_code==115:
        key="sup pressed"
    elif event.scan_code==114:
        key="sdown pressed"
    elif event.scan_code==165:
        key="sleft pressed"
    elif event.scan_code==163:
        key="sright pressed"
    elif event.scan_code==164:
        key="scentral pressed"    
#     print(event.name)
    else:
        key=event.name+" pressed"
#     print(key)
def func_keyup(event):
    global key
#     print('key down')
    if event.scan_code==115:
        key="sup released"
    elif event.scan_code==114:
        key="sdown released"    
    elif event.scan_code==165:
        key="sleft released"
    elif event.scan_code==163:
        key="sright released"
    elif event.scan_code==164:
        key="scentral released"
#     print(event.name)
    else:
        key=event.name+" released"
#     print(key)
keyboard.on_press_key("up",func_keydown,True)
keyboard.on_release_key("up",func_keyup,True)
keyboard.on_press_key("down",func_keydown,True)
keyboard.on_release_key("down",func_keyup,True)
keyboard.on_press_key("left",func_keydown,True)
keyboard.on_release_key("left",func_keyup,True)
keyboard.on_press_key("right",func_keydown,True)
keyboard.on_release_key("right",func_keyup,True)
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

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

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
    
myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
myEncoders.count1=0
myEncoders.count2=0
ENC1=0
ENC2=0
if myEncoders.connected == False:
    print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(0)
myEncoders.begin()

def task1(self):
    global myEncoders
    global myMotor
    global ENC1
    global ENC2
    global key
    global key_last
    
    SAMPLETIME = 0.1

    TARGET_R = 0
    TARGET_L = 0

#     KP = 0.011
    KP = 0.007
    KD = 0.0045
    KI = 0.00275
    R_MTR = 1
    L_MTR = 0
    FWD = 0
    BWD = 1
    
    m1_speed = 0
    m2_speed = 0
    e1_prev_error = 0
    e2_prev_error = 0
    e1_sum_error = 0
    e2_sum_error = 0
    
    yield
    
    while True:
        if key != '' and key_last != key:
            key_last=key
            myEncoders.count1=0
            myEncoders.count2=0
            
        if key=="up pressed":
            TARGET_R = 68
            TARGET_L = 68
#             myEncoders.count1=0
#             myEncoders.count2=0
        if key=="up released":
            TARGET_R=0
            TARGET_L=0
        if key=="down pressed":
            TARGET_R = -40
            TARGET_L = -40
        if key=="down released":
            TARGET_R=0
            TARGET_L=0
        if key=="left pressed":
            TARGET_R=40
            TARGET_L=-40
        if key=="left released":
            TARGET_R=0
            TARGET_L=0
        if key=="right pressed":
            TARGET_R=-40
            TARGET_L=40
        if key=="right released":
            TARGET_R=0
            TARGET_L=0
        
        e1_error = abs(TARGET_L) - abs(myEncoders.count1)
        e2_error = abs(TARGET_R) - abs(myEncoders.count2)
        m1_speed += (e1_error * KP * 255) + (e1_prev_error * KD) + (e1_sum_error * KI)
        m2_speed += (e2_error * KP * 255) + (e2_prev_error * KD) + (e2_sum_error * KI)
        m1_speed = max(min(255, m1_speed), 0)
        m2_speed = max(min(255, m2_speed), 0)
        
#         myMotor.set_drive(R_MTR,0 if TARGET_R > 0 else 1,m1_speed)
#         myMotor.set_drive(L_MTR,0 if TARGET_L > 0 else 1,m2_speed)
        if TARGET_L==0:
            myMotor.set_drive(L_MTR,0,0)
        else:
#             mot_B.throttle = m2_speed * (1 if TARGET_B > 0 else -1)
            if TARGET_L > 0:
                myMotor.set_drive(L_MTR,0,m1_speed)
            else:
                myMotor.set_drive(L_MTR,1,m1_speed)
        
        if TARGET_R==0:
            myMotor.set_drive(R_MTR,0,0)
        else:
#             mot_A.throttle = m1_speed * (1 if TARGET_A > 0 else -1)
            if TARGET_R > 0:
                myMotor.set_drive(R_MTR,0,m1_speed)
            else:
                myMotor.set_drive(R_MTR,1,m1_speed)
        
#             myMotor.set_drive(L_MTR,0 if TARGET_L > 0 else 1,m2_speed)
        
        print("Count1: %d, Count2: %s" % (myEncoders.count1, myEncoders.count2, ))
        ENC1=myEncoders.count1
        ENC2=myEncoders.count2
        myEncoders.count1=0
        myEncoders.count2=0

        yield [pyRTOS.timeout(SAMPLETIME)]
#         myEncoders.count1=0
#         myEncoders.count2=0
        e1_prev_error = e1_error
        e2_prev_error = e2_error
        e1_sum_error += e1_error
        e2_sum_error += e2_error
def task2(self):
    global draw
    global disp
    global image
    global ENC1
    global ENC2
    global key
    yield
    
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        enc="E1: " + str(ENC1)+",E2: "+str(ENC1)
        y = top
        draw.text((x, y), enc, font=font, fill="#FFFFFF")
        y += font.getsize(enc)[1]
        draw.text((x, y), "DIR: " + key, font=font, fill="#FFFFFF")
        disp.image(image, rotation)
        yield [pyRTOS.timeout(0.1)]
        
# def task3(self):
#     global key
#     yield
#     
#     while True:
#         if key:
#             print(key)
# #             key=''
# #         print("task2 ",a)
# #         print("task2")
#         yield [pyRTOS.timeout(0.1)]
def task3(self):
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
            
            if pos_v>90:
                pos_v=pos_v-1
            
            servo.move_servo_position(1, pos_v)
        if key=="sdown pressed":
            print(pos_v)
            
            if pos_v<130:
                pos_v=pos_v+1
            
            servo.move_servo_position(1, pos_v)
        if key=="sright pressed":
            print(pos_h)
            
            if pos_h>0:
                pos_h=pos_h-1
            
            servo.move_servo_position(0, pos_h)
        if key=="sleft pressed":
            print(pos_h)
            
            if pos_h<80:
                pos_h=pos_h+1
            
            servo.move_servo_position(0, pos_h)
        if key=="scentral pressed":
            print("center")
            pos_v=130
            pos_h=40  
            servo.move_servo_position(0, pos_h)
            servo.move_servo_position(1, pos_v)

        yield [pyRTOS.timeout(0.1)]
        
pyRTOS.add_task(pyRTOS.Task(task1))
# pyRTOS.add_task(pyRTOS.Task(task2))
pyRTOS.add_task(pyRTOS.Task(task3))

try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    print("Ending example.")
    myMotor.disable()
    backlight.value = False
    os.system("stty echo")
    print ("\n")
    sys.exit(0)



