from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from .models import *

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=10, message="Username must be between 4 and 10 characters")])
    email = StringField('email', validators=[InputRequired(message="Email required"), Length(min=8, max=30, message="Email must be between 4 and 20")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=6, max=14, message="Password must be between 6 and 14 characters")])
    confirm_password = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already exists")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=10, message="Username must be between 4 and 10 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=6, max=14, message="Password must be between 6 and 14 characters")])


class UserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=10, message="Username must be between 4 and 10 characters")])

class RoomForm(FlaskForm):
    room_name = StringField('room_name', validators=[InputRequired(message="Room name required"), Length(min=4, max=20, message="Room name must be between 4 and 20 characters")])
    users = StringField('users')

    def validate_room(self, room_name):
        room = Room.query.filter_by(room_name=room_name).first()
        if room:
            raise ValidationError("Room already exists")

    def validate_users(self, users):
        users = users.data.split(sep=" ")
        for user in users:
            user_db = User.query.filter_by(username=user).first()
            if not user_db:
                raise ValidationError(f"No user named {user}")


