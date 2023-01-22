import pi_servo_hat
import time

# Initialize Constructor
test = pi_servo_hat.PiServoHat()

# Restart Servo Hat (in case Hat is frozen/locked)
test.restart()

# Test Run
#########################################
# Moves servo position to 0 degrees (1ms), Channel 0
test.move_servo_position(1, 60)

# Pause 1 sec
# time.sleep(1)

# Moves servo position to 90 degrees (2ms), Channel 0
# test.move_servo_position(0, 90)

# Pause 1 sec
# time.sleep(1)

# Sweep
#########################################
# while True:
#     for i in range(0, 90):
#         print(i)
#         test.move_servo_position(0, i)
#         time.sleep(.001)
#     for i in range(90, 0, -1):
#         print(i)
#         test.move_servo_position(0, i)
#         time.sleep(.001)

