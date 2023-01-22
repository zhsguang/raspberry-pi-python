from __future__ import print_function
import time
import sys
import math
import qwiic_scmd
import qwiic_dual_encoder_reader

myMotor = qwiic_scmd.QwiicScmd()

def runExample():
    SAMPLETIME = 0.1
    TARGET = 68
    KP = 0.011
    KD = 0.0055
    KI = 0.00275
    
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

    m1_speed = 0
    m2_speed = 0
    e1_prev_error = 0
    e2_prev_error = 0
    e1_sum_error = 0
    e2_sum_error = 0
    
    while True:
        e1_error = TARGET - abs(myEncoders.count1)
        e2_error = TARGET - abs(myEncoders.count2)
#         m1_speed += e1_error * KP * 255
        m1_speed += (e1_error * KP * 255) + (e1_prev_error * KD) + (e1_sum_error * KI)
        m2_speed += (e2_error * KP * 255) + (e2_prev_error * KD) + (e2_sum_error * KI)
        m1_speed = max(min(255, m1_speed), 0)
        m2_speed = max(min(255, m2_speed), 0)
#         speed = 150
        
        myMotor.set_drive(R_MTR,FWD,m1_speed)
        myMotor.set_drive(L_MTR,FWD,m2_speed)
        print("Count1: %d, Count2: %s" % (myEncoders.count1, myEncoders.count2, ))
        myEncoders.count1=0
        myEncoders.count2=0
        time.sleep(SAMPLETIME)
        
        e1_prev_error = e1_error
        e2_prev_error = e2_error
        e1_sum_error += e1_error
        e2_sum_error += e2_error
if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        myMotor.disable()
        sys.exit(0)


