import eventlet
import socketio
from a_star import AStar
import threading
import json
import RPi.GPIO as GPIO
from PCA9685 import PCA9685

# All the text displays after 3 seconds

# def foo():
#     print(time.ctime())
#     threading.Timer(1, foo).start()


# foo()

# my_timer = threading.Timer(3.0, mytimer)
pwm = PCA9685()
pwm.setPWMFreq(50)
# pwm.setServoPulse(1,500)
v_pos = 90
h_pos = 90
pwm.setRotationAngle(1, v_pos)
pwm.setRotationAngle(0, h_pos)

a_star = AStar()
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


# def mytimer():
#     print("Demo Python Program\n")
#     sio.emit('my event', {'data': 'foobar'})
#     threading.Timer(1, mytimer).start()

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('my event', {'data': 'foobar'})
    # my_timer = threading.Timer(1.0, mytimer)
    # my_timer.start()
    # mytimer()


@sio.event
def my_message(sid, data):
    global v_pos
    global h_pos

    print('message ', data)
    if data == "up pressed":
        a_star.motors(-400, -400)
        # sio.emit('my event', {'data': 'foobar'})
    if data == "up released":
        a_star.motors(0, 0)
    if data == "down pressed":
        a_star.motors(300, 300)
    if data == "down released":
        a_star.motors(0, 0)
    if data == "left pressed":
        a_star.motors(-200, 200)
    if data == "left released":
        a_star.motors(0, 0)
    if data == "right pressed":
        a_star.motors(200, -200)
    if data == "right released":
        a_star.motors(0, 0)
    if data == "W pressed":
        print("servo up")
    if data == "A pressed":
        print("servo left")
        if h_pos < 170:
            h_pos = h_pos + 1
            pwm.setRotationAngle(0, h_pos)
    if data == "D pressed":
        print("servo right")
        if h_pos > 10:
            h_pos = h_pos - 1
            pwm.setRotationAngle(0, h_pos)
    if data == "S pressed":
        print("servo down")
        if v_pos < 170:
            v_pos = v_pos + 1
            pwm.setRotationAngle(1, v_pos)
    if data == "W pressed":
        print("servo up")
        if v_pos > 10:
            v_pos = v_pos - 1
            pwm.setRotationAngle(1, v_pos)
    if data == "servo reset":
        print("servo reset")
        v_pos =90
        h_pos = 90
        pwm.setRotationAngle(0, h_pos)
        pwm.setRotationAngle(1, v_pos)

    if data == "get_status":
        encoders = a_star.read_encoders()
        # print(encoders[0], ',', encoders[1])
        enc = {'enc1': encoders[0], 'enc2': encoders[1]}
        st = json.dumps(enc)
        # print(st)
        sio.emit('my_message', st)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
