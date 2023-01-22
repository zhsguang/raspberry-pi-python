from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys
import pyRTOS

myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
if myEncoders.connected == False:
    print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    sys.exit(0)
myEncoders.begin()
def task1(self):
#     ledpin1 = machine.Pin(0, machine.Pin.OUT)
#     ledpin1.value(0)
    global myEncoders
    yield
    
    while True:
        print("Count1: %d, Count2: %s" % (myEncoders.count1, myEncoders.count2, ))
#         ledpin1.toggle()
        yield [pyRTOS.timeout(0.1)]

def task2(self):
#     ledpin2 = machine.Pin(1, machine.Pin.OUT)
#     ledpin2.value(0)
    yield
    
    while True:
        print("task2")
#         ledpin2.toggle()
        yield [pyRTOS.timeout(1)]
    
pyRTOS.add_task(pyRTOS.Task(task1))
# pyRTOS.add_task(pyRTOS.Task(task2))


pyRTOS.start()