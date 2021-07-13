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
        room = msg["room"]
        send({"message": message, "username": current_user.username}, room=room)

@socketio.on('join')
def on_join(data):
    user = data["username"]
    room = data["room"]
    join_room(room)
    emit("room-manager", {"message": f"{user} has joined the {room} room"}, room=room)

@socketio.on('leave')
def on_leave(data):
    user = data["username"]
    room = data["room"]
    leave_room(room)
    emit("room-manager", {"message": f"{user} has left the {room} room"}, room=room)












