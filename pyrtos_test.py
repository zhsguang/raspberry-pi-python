import pyRTOS
import keyboard
import os

os.system("stty -echo")
# a=100
key=''
def func_keydown(event):
    global key
#     print('key down')
    print(event.name)
    key=event.name+" down"
def func_keyup(event):
    global key
#     print('key down')
    print(event.name)
    key=event.name+" release"
keyboard.on_press_key("up",func_keydown,True)
keyboard.on_release_key("up",func_keyup,True)
# keyboard.on_release(func_keyup)
def task1(self):
#     ledpin1 = machine.Pin(0, machine.Pin.OUT)
#     ledpin1.value(0)
    global key
    yield
    
    while True:
        if keyboard.is_pressed('a'):  # if key 'q' is pressed 
            print('a Pressed')
            key="a"
#         print("task1 ",a)
#         a=a-1
#         ledpin1.toggle()
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
    
# pyRTOS.add_task(pyRTOS.Task(task1))
pyRTOS.add_task(pyRTOS.Task(task2))

try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    os.system("stty echo")
    print ("\n")
    sys.exit(0)