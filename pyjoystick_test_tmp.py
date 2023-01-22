from pyjoystick.sdl2 import Key, Joystick, run_event_loop

def print_add(joy):
    print('Added', joy)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    print('Key:', key.keyname)
    # print(dir(key))
    if key.keyname=="Up":
        print("UP")
    if key=="Hat 0 [Centered]":
        print("STOP")
    

run_event_loop(print_add, print_remove, key_received)