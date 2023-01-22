from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys
import pyRTOS
import qwiic_scmd

myMotor = qwiic_scmd.QwiicScmd()
if myMotor.connected == False:
    print("Motor Driver not connected. Check connections.", \
        file=sys.stderr)
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
if myEncoders.connected == False:
    print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(0)
myEncoders.begin()
myMotor.set_drive(0,0,250)
myMotor.set_drive(1,0,250)
def task1(self):
#     ledpin1 = machine.Pin(0, machine.Pin.OUT)
#     ledpin1.value(0)
    global myEncoders
    yield
    
    while True:
        print("Count1: %d, Count2: %s" % (myEncoders.count1, myEncoders.count2, ))
        myEncoders.count1=0
        myEncoders.count2=0
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


# pyRTOS.start()

try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    print("Ending example.")
    myMotor.disable()
    sys.exit(0)
