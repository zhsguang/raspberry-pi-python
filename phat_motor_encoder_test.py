from __future__ import print_function
import time
import sys
import math
import qwiic_scmd
import qwiic_dual_encoder_reader

myMotor = qwiic_scmd.QwiicScmd()

def runExample():
    myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
    if myEncoders.connected == False:
        print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", file=sys.stderr)
        sys.exit(0)

    myEncoders.begin()
    myEncoders.count1=0
    myEncoders.count2=0
    print("Motor Test.")
    R_MTR = 0
    L_MTR = 1
    FWD = 0
    BWD = 1

    if myMotor.connected == False:
        print("Motor Driver not connected. Check connections.", \
            file=sys.stderr)
        return
    myMotor.begin()
    print("Motor initialized.")
    time.sleep(.250)

    # Zero Motor Speeds
    myMotor.set_drive(0,0,0)
    myMotor.set_drive(1,0,0)

    myMotor.enable()
    print("Motor enabled")
    time.sleep(.250)


    while True:
        speed = 250
        myMotor.set_drive(L_MTR,FWD,speed)
        myMotor.set_drive(R_MTR,FWD,speed)
        print("Count1: %d, Count2: %s" % (myEncoders.count1, myEncoders.count2, ))
        myEncoders.count1=0
        myEncoders.count2=0
        time.sleep(0.1)
        

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        myMotor.disable()
        sys.exit(0)

