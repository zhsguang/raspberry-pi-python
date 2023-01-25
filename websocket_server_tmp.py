from flask import Flask, render_template
from flask_socketio import SocketIO, emit

appFlask = Flask(__name__)
socketio = SocketIO(appFlask,cors_allowed_origins='*')


@appFlask.route('/')
def index():


    return render_template('websocket.html')


@socketio.on('connect')
def test_connect():


    socketio.emit('after connect', {'data': 'Let us learn Web Socket in Flask'})
if __name__ == '__main__':
    socketio.run(appFlask,host="0.0.0.0")
