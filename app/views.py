from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_login import current_user
from .models import *
from .wtform_fields import RoomForm

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)

@views.route("/chat", methods=["GET", "POST"])
def chat():
    lobby_room = Room.query.filter_by(room_name="Lobby").first()
    if not lobby_room:
        lobby_room = Room(room_name="Lobby")
        db.session.add(lobby_room)
        for user in User.query.all():
            lobby_room.members.append(user)
        db.session.commit()
    elif current_user not in lobby_room.members:
        lobby_room.members.append(current_user)
        db.session.commit()
    elif len(lobby_room.messages) >= 100:
        db.session.delete(lobby_room.messages[0])
        db.session.commit()

    return render_template("chat.html", user=current_user, rooms=current_user.rooms, current_room=Room.query.filter_by(room_name=session["current_room"]).first())

@views.route("/create-room", methods=["GET", "POST"])
def create_room():
    if current_user.is_authenticated:
        room_form = RoomForm()
        if room_form.validate_on_submit():
            users = room_form.users.data.split(sep=" ")
            room_name = room_form.room_name.data
            room = Room(room_name=room_name, owner=current_user.username)
            db.session.add(room)
            if current_user.username not in users:
                room.members.append(current_user)
            for user in users:
                user = User.query.filter_by(username=user).first()
                room.members.append(user)
            db.session.commit()
            flash(f"{room_name} was created successfully", category="success")
            return redirect(url_for("views.chat"))
        else:
            for error in room_form.errors.values():
                flash(error[0], category="error")
        return render_template("create_room.html", user=current_user, form=room_form)
    return redirect(url_for("views.index"))




