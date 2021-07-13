from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .models import *
from .wtform_fields import RoomForm

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)

@views.route("/chat", methods=["GET", "POST"])
def chat():
    rooms = Room.query.all()
    return render_template("chat.html", user=current_user, rooms=rooms)

@views.route("/create-room", methods=["GET", "POST"])
def create_room():
    if current_user.is_authenticated:
        room_form = RoomForm()
        if room_form.validate_on_submit():
            users = room_form.users.data.split(sep=" ")
            room_name = room_form.room_name.data
            room = Room(room_name=room_name, owner=current_user.username)
            db.session.add(room)
            db.session.commit()
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


def create():
    #room1 = Room.query.filter_by(room_name="test1").first()
    #user2 = User.query.filter_by(username="user2").first()

    #room1.members.append(user2)

    #db.session.commit()

    #for room in user2.rooms:
       # print(room.room_name)


    #user1 = User(username="user1")
    #user2 = User(username="user2")

    room1 = Room(room_name="test1")
    room2 = Room(room_name="test2")

    #db.session.add(user1)
    #db.session.add(user2)
    db.session.add(room1)
    db.session.add(room2)

    db.session.commit()










