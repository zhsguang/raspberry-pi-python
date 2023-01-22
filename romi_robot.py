import keyboard
from my_a_star import AStar
import time
import pyRTOS
import sys
import os

a_star = AStar()
speed=300
tspeed=200

os.system("stty -echo")

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



def task1(self):
    global key
    yield
    
    while True:
        if key=="up pressed":
            print(key)
            a_star.motors(-speed, -speed)

        if key=="up released":
            print(key)
            a_star.motors(0, 0)

        if key=="down pressed":
            print(key)
            a_star.motors(speed, speed)

        if key=="down released":
            print(key)
            a_star.motors(0, 0)

        if key=="left pressed":
            print(key)
            a_star.motors(-tspeed, tspeed)

        if key=="left released":
            print(key)
            a_star.motors(0, 0)

        if key=="right pressed":
            print(key)
            a_star.motors(tspeed, -tspeed)

        if key=="right released":
            print(key)
            a_star.motors(0, 0)
        
        yield [pyRTOS.timeout(0.1)]

pyRTOS.add_task(pyRTOS.Task(task1))

try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    print("Ending example.")
    a_star.motors(0, 0)
    os.system("stty echo")
    print ("\n")
    sys.exit(0) 
# print("Press ESC to stop.")
# keyboard.wait('esc')