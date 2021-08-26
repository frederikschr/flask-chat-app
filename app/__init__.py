from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from .models import *
from flask_restful import Api
from .resources import jwt
from .resources import *
import os

app = Flask(__name__)

def create_app():
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SESSION_TYPE"] = "filesystem"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    login_manager = LoginManager(app)

    Session(app)

    register_resources()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    db.init_app(app)

    jwt.init_app(app)

    from .socket import socketio

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    create_database(app)

    return socketio, app

def register_resources():
    api = Api(app)

    api.add_resource(CreateAccessToken, "/api/token")

    api.add_resource(MyUser, "/api/user/me")

    api.add_resource(OneUser, "/api/user/one")
    api.add_resource(AllUsers, "/api/user/all")

    api.add_resource(OneMessage, "/api/message/one")
    api.add_resource(ALlMessages, "/api/message/all")

    api.add_resource(OneRoom, "/api/room/one")
    api.add_resource(ALlRooms, "/api/room/all")

def create_database(app):
    db.create_all(app=app)
    print("Created database")
    create_admin(app)