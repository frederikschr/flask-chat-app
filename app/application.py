from flask import session, request
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from app import app
from flask_login import current_user
from .models import *

socketio = SocketIO(app, manage_session=False)
client_sid = {}

def create_message(author, content, room, is_system_message=False):
    message = Message(author=author, content=content, room_id=Room.query.filter_by(room_name=room).first().id, is_system_message=is_system_message)
    db.session.add(message)
    for user in Room.query.filter_by(room_name=room).first().members:
        message.receivers.append(user)
    db.session.commit()

@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        client_sid[current_user.username] = request.sid

@socketio.on('message')
def on_message(msg):
    if current_user.is_authenticated:
        user = msg["username"]
        message = msg["message"]
        room = msg["room"]
        create_message(user, message, room)
        send({"message": message, "username": user}, room=room)

@socketio.on('member-removed')
def on_member_removed(data):
    user = current_user.username
    member = data["member"]
    room = data["room"]
    message = f"{user} has removed {member} from {room}"
    emit("room-manager", {"message": message}, room=room)
    create_message(None, message, room, is_system_message=True)
    emit("room-leave", room=client_sid[member])
    emit("refresh", room=room)

@socketio.on('room-deleted')
def on_room_deleted(data):
    room = data["room"]
    emit("room-leave", room=room)
    emit("refresh")

@socketio.on('room-change')
def on_room_change(data):
    room = data["room"]
    session["current_room"] = room

@socketio.on('join')
def on_join(data):
    if Room.query.filter_by(room_name=data["room"]).first():
        user = data["username"]
        room = data["room"]
        join_room(room)
        message = f"{user} has joined the {room} room"
        create_message(None, message, room, is_system_message=True)
        emit("room-manager", {"message": message}, room=room)

@socketio.on('leave')
def on_leave(data):
    if Room.query.filter_by(room_name=data["room"]).first():
        user = data["username"]
        room = data["room"]
        leave_room(room)
        message = f"{user} has left the {room} room"
        create_message(None, message, room, is_system_message=True)
        emit("room-manager", {"message": message}, room=room)












