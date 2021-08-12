from flask import session, request, flash
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

@socketio.on("member-added")
def on_member_added(data):
    new_member, room = data["new_member"], data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    new_member_db = User.query.filter_by(username=new_member).first()
    if new_member_db:
        if current_user.username == room_db.owner:
            if room_db not in new_member_db.rooms:
                room_db.members.append(new_member_db)
                db.session.commit()
                flash(f"Successfully added {new_member} to {room}", category="success")
                if new_member in client_sid:
                    emit("refresh", room=client_sid[new_member])
                emit("refresh", room=room)
            else:
                flash(f"{new_member} is already in {room}", category="error")
    else:
        flash(f"No user named {new_member}", category="error")

@socketio.on('member-removed')
def on_member_removed(data):
    user = current_user.username
    member, room = data["member"], data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    member_db = User.query.filter_by(username=member).first()
    if current_user.username == room_db.owner:
        room_db.members.remove(member_db)
        db.session.commit()
        flash(f"Successfully removed {member} from {room}", category="success")
        message = f"{user} has removed {member} from {room}"
        emit("room-manager", {"message": message}, room=room)
        create_message(None, message, room, is_system_message=True)
        if member in client_sid:
            emit("room-leave", room=client_sid[member])
        emit("refresh", room=room)

@socketio.on('room-deleted')
def on_room_deleted(data):
    room = data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    if room_db.owner == current_user.username:
        db.session.delete(room_db)
        db.session.commit()
        flash(f"successfully deleted {room}", category="success")
        emit("room-leave", room=room)

@socketio.on('room-change')
def on_room_change(data):
    room = data["room"]
    session["current_room"] = room

@socketio.on('room-cleared')
def on_room_cleared(data):
    room = data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    if room_db.owner == current_user.username:
        for message in room_db.messages:
            db.session.delete(message)
        db.session.commit()
        flash(f"Successfully cleared {room}", category="success")
        emit("refresh", room=room)

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












