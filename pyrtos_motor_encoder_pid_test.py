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
# import threading


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
    
    SAMPLETIME = 0.1
    TARGET = -150
    KP = 0.002
    KD = 0.001
    KI = 0.0005
    
    R_MTR = 0
    L_MTR = 1
    FWD = 0
    BWD = 1
    
    m1_speed = 100
    m2_speed = 100
    e1_prev_error = 0
    e2_prev_error = 0
    e1_sum_error = 0
    e2_sum_error = 0
    
    yield
    
    while True:
        e1_error = abs(TARGET) - abs(myEncoders.count1)
        e2_error = abs(TARGET) - abs(myEncoders.count2)

        m1_speed += (e1_error * KP * 255) + (e1_prev_error * KD) + (e1_sum_error * KI)
        m2_speed += (e2_error * KP * 255) + (e2_prev_error * KD) + (e2_sum_error * KI)
        m1_speed = max(min(255, m1_speed), 0)
        m2_speed = max(min(255, m2_speed), 0)
        
        myMotor.set_drive(R_MTR,0 if TARGET > 0 else 1,m1_speed)
        myMotor.set_drive(L_MTR,0 if TARGET > 0 else 1,m2_speed)
        print("Count1: %d, Count2: %s" % (myEncoders.count1, myEncoders.count2, ))
        ENC1=myEncoders.count1
        ENC2=myEncoders.count2
        myEncoders.count1=0
        myEncoders.count2=0

        yield [pyRTOS.timeout(SAMPLETIME)]
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
    yield
    
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        y = top
        draw.text((x, y), "E1: " + str(ENC1)+",E2: "+str(ENC1), font=font, fill="#FFFFFF")

        disp.image(image, rotation)
        yield [pyRTOS.timeout(0.1)]
    
pyRTOS.add_task(pyRTOS.Task(task1))
pyRTOS.add_task(pyRTOS.Task(task2))


try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    print("Ending example.")
    myMotor.disable()
    backlight.value = False
    sys.exit(0)

