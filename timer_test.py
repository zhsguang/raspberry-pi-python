import time, threading


def foo():
    print(time.ctime())
    threading.Timer(1, foo).start()


foo()
