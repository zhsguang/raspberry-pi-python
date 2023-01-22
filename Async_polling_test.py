#!/usr/bin/env python
# coding: utf-8

# Load the gamepad and time libraries
import Gamepad
import time

# Gamepad settings
gamepadType = Gamepad.XboxONE
buttonHappy = 'A'
buttonBeep = 'B'
# buttonExit = 'PS'
joystickSpeed = 'LAS -Y'
joystickSteering = 'RAS -X'
pollInterval = 0.1

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

# Start the background updating
gamepad.startBackgroundUpdates()

# Joystick events handled in the background
try:
    while gamepad.isConnected():
        # Check for the exit button
        # if gamepad.beenPressed(buttonExit):
        #     print('EXIT')
        #     break

        # Check for happy button changes
        if gamepad.beenPressed('A'):
            # print(':)')
            # gamepad.BUTTON('A')
            print('A pressed')
        if gamepad.beenReleased('A'):
            print('A released')

        # Check if the beep button is held
        if gamepad.isPressed(buttonBeep):
            print('BEEP')

        # Update the joystick positions
        # Speed control (inverted)
        speed = -gamepad.axis('DPAD -X')
        print(speed)
        # Steering control (not inverted)
        # steering = gamepad.axis(joystickSteering)
        # print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))

        # Sleep for our polling interval
        time.sleep(pollInterval)
finally:
    # Ensure the background thread is always terminated when we are done
    gamepad.disconnect()
