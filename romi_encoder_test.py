from my_a_star import AStar
import time

a_star = AStar()
a_star.reset_encoders()
# encoders = a_star.read_encoders()
# print(encoders[0],',',encoders[1])
a_star.motors(300, 300)

# encoders=a_star.read_encoders()
# time.sleep(2)
# a_star.motors(0, 0)
try:
    # encoders=a_star.read_encoders()
    # a_star.play_notes("l16ceg>c")
    # print(encoders[0],',',encoders[1])
    # a_star.motors(0, 0)
    while True:
        encoders=a_star.read_encoders()
        print(encoders[0],',',encoders[1])
        time.sleep(1)
        a_star.reset_encoders()
        
        # encoders[0]=0
        # encoders[1]=0
except:
    a_star.motors(0, 0)