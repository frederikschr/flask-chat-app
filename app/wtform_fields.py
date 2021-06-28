from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from .models import User

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