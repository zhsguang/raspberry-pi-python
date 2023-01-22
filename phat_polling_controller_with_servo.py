#!/usr/bin/env python
# coding: utf-8

# Load the gamepad and time libraries

from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys
import pyRTOS
import qwiic_scmd
import subprocess
import Gamepad
import pi_servo_hat

# Gamepad settings
gamepadType = Gamepad.XboxONE
buttonHappy = 'A'
buttonBeep = 'B'
buttonExit = 'HOME'
joystickSpeed = 'LAS -Y'
joystickSteering = 'RAS -X'

R_MTR = 0
L_MTR = 1
FWD = 0
BWD = 1
mspeed=250
tspeed=180
key=''
pollInterval = 0.1

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

myServo = pi_servo_hat.PiServoHat()
myServo.restart()
s0_pos=90
s1_pos=90

myServo.move_servo_position(0, s0_pos)
myServo.move_servo_position(1, s1_pos)
# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# Set some initial state
speed = 0.0
steering = 0.0
gamepad.startBackgroundUpdates()
# Handle joystick updates one at a time
try:
    while gamepad.isConnected():
        if gamepad.beenPressed('A'):
            # print(':)')
            # gamepad.BUTTON('A')
            print('A pressed')
        if gamepad.beenReleased('A'):
            print('A released')
        if gamepad.axis('DPAD -X')==-1.0:
            print('Left')
        elif gamepad.axis('DPAD -X')==1.0:
            print('Right')
        elif gamepad.axis('DPAD -Y')==-1.0:
            print('Up')
            myMotor.set_drive(L_MTR,FWD,mspeed)
            myMotor.set_drive(R_MTR,FWD,mspeed)
        elif gamepad.axis('DPAD -Y')==1.0:
            print('Down')
        else:
            print('Stop')
            myMotor.set_drive(0,0,0)
            myMotor.set_drive(1,0,0)
        # Wait for the next event
        # eventType, control, value = gamepad.getNextEvent()

        # Determine the type
        # if eventType == 'BUTTON':
        #     print(control)
        #     # Button changed
        #     if control == 'B':
        #         # Happy button (event on press and release)
        #         if value:
        #             print('A on')
        #             if s0_pos>0:
        #                 s0_pos=s0_pos-1
        #             myServo.move_servo_position(0, s0_pos)
        #         else:
        #             print('A off')
        #     elif control == 'A':
        #         # Beep button (event on press)
        #         if value:
        #             print('B on')
        #         else:
        #             print('B off')
        #     elif control == 'X':
        #         # Beep button (event on press)
        #         if value:
        #             print('X on')
        #         else:
        #             print('X off')
        #     elif control == 2:
        #         # Beep button (event on press)
        #         if value:
        #             print('Y on')
        #             if s0_pos<180:
        #                 s0_pos=s0_pos+1
        #             myServo.move_servo_position(0, s0_pos)

                    
        #         else:
        #             print('Y off')
        # elif eventType == 'AXIS':
        #     # Joystick changed
        #     if control == joystickSpeed:
        #         # Speed control (inverted)
        #         speed = -value
        #     elif control == joystickSteering:
        #         # Steering control (not inverted)
        #         steering = value
        #     elif control == 'DPAD -X':
        #         # print('Dpad x:',value)
        #         if value == -1.0:
        #             print("LEFT")
        #             myMotor.set_drive(L_MTR,FWD,tspeed)
        #             myMotor.set_drive(R_MTR,BWD,tspeed)
        #         if value == 1.0:
        #             print("RIGHT")
        #             myMotor.set_drive(L_MTR,BWD,tspeed)
        #             myMotor.set_drive(R_MTR,FWD,tspeed)
        #         if value == 0.0:
        #             print("STOP")
        #             myMotor.set_drive(0,0,0)
        #             myMotor.set_drive(1,0,0)
        #     elif control == 'DPAD -Y':
        #         if value == -1.0:
        #             print("UP")
        #             myMotor.set_drive(L_MTR,FWD,mspeed)
        #             myMotor.set_drive(R_MTR,FWD,mspeed)
        #         if value == 1.0:
        #             print("DOWN")
        #             myMotor.set_drive(L_MTR,BWD,mspeed)
        #             myMotor.set_drive(R_MTR,BWD,mspeed)
        #         if value == 0.0:
        #             print("STOP")
        #             myMotor.set_drive(0,0,0)
        #             myMotor.set_drive(1,0,0)
                # print('Dpad y:',value)
            # print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))
        time.sleep(pollInterval)
finally:
    # Ensure the background thread is always terminated when we are done
    gamepad.disconnect()
