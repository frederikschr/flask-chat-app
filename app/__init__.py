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
    #app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SECRET_KEY"] = "secret!"
    app.config["SESSION_TYPE"] = "filesystem"
    #app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://inlnknrtcojulh:37393be7c16b1a5910e8d62dbb036352a31770f2c7102df17657c577e64d3cc8@ec2-52-214-178-113.eu-west-1.compute.amazonaws.com:5432/d99127gk3g45hf"

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

    api.add_resource(GetAllUsers, "/api/get-users")
    api.add_resource(GetOneUser, "/api/get-user/<id>")
    api.add_resource(CreateAccessToken, "/api/token")
    api.add_resource(GetMyPassword, "/api/me")
    api.add_resource(GetAllUserMessages, "/api/messages")
    api.add_resource(GetUserContent, "/api/message/<username>/<content>")

def create_database(app):
    db.create_all(app=app)
    print("Created database")
