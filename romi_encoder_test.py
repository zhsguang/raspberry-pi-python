from my_a_star import AStar
import time
import json

a_star = AStar()
a_star.reset_encoders()
# encoders = a_star.read_encoders()
# print(encoders[0],',',encoders[1])
a_star.motors(300, 300)
# time.sleep(2)
# encoders=a_star.read_encoders()
time.sleep(2)
# a_star.motors(0, 0)
try:
    # encoders=a_star.read_encoders()
    # a_star.play_notes("l16ceg>c")
    # print(encoders[0],',',encoders[1])
    # a_star.motors(0, 0)

    encoders = a_star.read_encoders()
    print(encoders[0], ',', encoders[1])
    enc = {'enc1': encoders[0], 'enc2': encoders[1]}
    print(json.dumps(enc))
    a_star.motors(0, 0)

        # encoders[0]=0
        # encoders[1]=0
except:
    a_star.motors(0, 0)
