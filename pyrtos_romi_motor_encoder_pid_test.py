import keyboard
from my_a_star import AStar
import time
import pyRTOS
import sys
import os

a_star = AStar()
a_star.reset_encoders()
# a_star.motors(300, 300)


ENC1=0
ENC2=0

def task1(self):
    global myEncoders
    global myMotor
    global ENC1
    global ENC2
    
    SAMPLETIME = 0.1
    TARGET = 250
    KP = 0.002
    KD = 0.001
    KI = 0.0005
    
    R_MTR = 0
    L_MTR = 1
    FWD = 0
    BWD = 1
    
    # m1_speed = 100
    # m2_speed = 100
    e1_prev_error = 0
    e2_prev_error = 0
    e1_sum_error = 0
    e2_sum_error = 0
    
    yield
    
    while True:
        encoders=a_star.read_encoders()
        
        e1_error = abs(TARGET) - abs(encoders[0])
        e2_error = abs(TARGET) - abs(encoders[1])

        m1_speed += (e1_error * KP * 255) + (e1_prev_error * KD) + (e1_sum_error * KI)
        m2_speed += (e2_error * KP * 255) + (e2_prev_error * KD) + (e2_sum_error * KI)
        m1_speed = max(min(300, m1_speed), 0)
        m2_speed = max(min(300, m2_speed), 0)
        a_star.motors(m1_speed, m2_speed)
        # myMotor.set_drive(R_MTR,0 if TARGET > 0 else 1,m1_speed)
        # myMotor.set_drive(L_MTR,0 if TARGET > 0 else 1,m2_speed)
        print("Count1: %d, Count2: %s" % (encoders[0], encoders[1], ))
        # print(encoders[0],',',encoders[1])
        # ENC1=myEncoders.count1
        # ENC2=myEncoders.count2
        a_star.reset_encoders()

        yield [pyRTOS.timeout(SAMPLETIME)]
        e1_prev_error = e1_error
        e2_prev_error = e2_error
        e1_sum_error += e1_error
        e2_sum_error += e2_error
def task2(self):
    global draw
    global disp
    global image
    global ENC1
    global ENC2
    yield
    
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        y = top
        draw.text((x, y), "E1: " + str(ENC1)+",E2: "+str(ENC1), font=font, fill="#FFFFFF")

        disp.image(image, rotation)
        yield [pyRTOS.timeout(0.1)]
    
pyRTOS.add_task(pyRTOS.Task(task1))
pyRTOS.add_task(pyRTOS.Task(task2))


try:
    pyRTOS.start()
except (KeyboardInterrupt, SystemExit) as exErr:
    print("Ending example.")
    myMotor.disable()
    backlight.value = False
    sys.exit(0)

