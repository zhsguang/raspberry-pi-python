from my_a_star import AStar
import time

a_star = AStar()
a_star.motors(300, 300)
time.sleep(2)
a_star.motors(0, 0)