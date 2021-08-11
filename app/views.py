from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_required
from .models import *
from .wtform_fields import RoomForm
import ast

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
            if current_user not in users:
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

@views.route("/delete-room", methods=["POST"])
@login_required
def delete_room():
    data = request.data
    dict = data.decode("UTF-8")
    data = ast.literal_eval(dict)
    room = data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    if room_db.owner == current_user.username:
        db.session.delete(room_db)
        db.session.commit()
        flash(f"successfully deleted {room}", category="success")
    return redirect(url_for("views.index"))

@views.route("/clear-room", methods=["POST"])
@login_required
def clear_room():
    data = request.data
    dict = data.decode("UTF-8")
    data = ast.literal_eval(dict)
    room = data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    if room_db.owner == current_user.username:
        for message in room_db.messages:
            db.session.delete(message)
        db.session.commit()
        flash(f"Successfully cleared {room}", category="success")
    return redirect(url_for("views.index"))

@views.route("/remove-member", methods=["POST"])
@login_required
def remove_member():
    data = request.data
    dict = data.decode("UTF-8")
    data = ast.literal_eval(dict)
    member, room = data["member"], data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    member_db = User.query.filter_by(username=member).first()
    if current_user.username == room_db.owner:
        room_db.members.remove(member_db)
        db.session.commit()
        flash(f"Successfully removed {member} from {room}", category="success")
    return redirect(url_for("views.chat"))

@views.route("/add-member", methods=["POST"])
@login_required
def add_member():
    data = request.data
    dict = data.decode("UTF-8")
    data = ast.literal_eval(dict)
    new_member, room = data["new_member"], data["room"]
    room_db = Room.query.filter_by(room_name=room).first()
    new_member_db = User.query.filter_by(username=new_member).first()
    if new_member_db:
        if current_user.username == room_db.owner:
            if room_db not in new_member_db.rooms:
                room_db.members.append(new_member_db)
                db.session.commit()
                flash(f"Successfully added {new_member} to {room}", category="success")
            else:
                flash(f"{new_member} is already in {room}", category="error")
    else:
        flash(f"No user named {new_member}", category="error")
    return redirect(url_for("views.chat"))



