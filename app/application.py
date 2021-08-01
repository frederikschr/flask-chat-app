from flask import session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from app import app
from flask_login import current_user
from .models import *

socketio = SocketIO(app, manage_session=False)

def create_message(username, content, room, is_system_message=False):
    new_message = Message(author=User.query.filter_by(username=username).first().username, content=content, room_id=Room.query.filter_by(room_name=room).first().id, is_system_message=is_system_message)
    db.session.add(new_message)
    db.session.commit()

@socketio.on('connect')
def on_connect():
    print("Client connected")

@socketio.on('message')
def on_message(msg):
    if current_user.is_authenticated:
        user = msg["username"]
        message = msg["message"]
        room = msg["room"]
        create_message(user, message, room)
        send({"message": message, "username": user}, room=room)

@socketio.on('join')
def on_join(data):
    user = data["username"]
    room = data["room"]
    join_room(room)
    session["current_room"] = room
    message = f"{user} has joined the {room} room"
    create_message(user, message, room, is_system_message=True)
    emit("room-manager", {"message": message}, room=room)

@socketio.on('leave')
def on_leave(data):
    user = data["username"]
    room = data["room"]
    leave_room(room)
    message = f"{user} has left the {room} room"
    create_message(user, message, room, is_system_message=True)
    emit("room-manager", {"message": message}, room=room)












