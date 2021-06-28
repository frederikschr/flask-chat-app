from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_login import LoginManager
from .models import *
from os import path

app = Flask(__name__)

def create_app():
    app.config["SECRET_KEY"] = "secret!"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    db.init_app(app)

    from .application import socketio

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    create_database(app)

    return socketio, app

def create_database(app):
    if not path.exists(f"app/{DB_NAME}"):
        db.create_all(app=app)
        print("Created database")
