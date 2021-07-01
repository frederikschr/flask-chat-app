from flask_socketio import SocketIO, emit, send, join_room, leave_room
from app import app
from flask_login import current_user

socketio = SocketIO(app)

@socketio.on('connect')
def on_connect():
    print("Client connected")


@socketio.on('message')
def on_message(msg):
    if current_user.is_authenticated:
        message = msg["message"]
        send({"message": message, "username": current_user.username}, broadcast=True)




