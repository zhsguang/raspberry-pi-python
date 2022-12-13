from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys
import qwiic_scmd

myMotor = qwiic_scmd.QwiicScmd()

def runExample():
    print("Motor Test.")
    R_MTR = 1
    L_MTR = 0
    FWD = 0
    BWD = 1
    
    if myMotor.connected == False:
        print("Motor Driver not connected. Check connections.", \
            file=sys.stderr)
        return
    myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
    if myEncoders.connected == False:
        print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    myEncoders.begin()
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
        speed = 255
        myEncoders.count1=0
        myMotor.set_drive(0,FWD,speed)
        time.sleep(.1)
        print(myEncoders.count1)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        myMotor.disable()
        sys.exit(0)

