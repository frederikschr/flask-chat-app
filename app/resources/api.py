from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from app.models import User
from werkzeug.security import check_password_hash

class CreateAccessToken(Resource):
    def get(self):
        json_data = request.get_json()

        username = json_data["username"]
        password = json_data["password"]

        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, HTTPStatus.OK

class GetMyPassword(Resource):
    @jwt_required
    def get(self):

        print(get_jwt_identity())

        user = User.query.filter_by(id=get_jwt_identity()).first()

        return {"password": user.password}

class GetAllUsers(Resource):
    def get(self):
        users = []
        for user in User.query.all():
            user_dict = {}
            user_dict["username"] = user.username
            user_dict["id"] = user.id
            users.append(user_dict)
        return users

class GetOneUser(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {"username": user.username, "id": user.id}

class GetAllUserMessages(Resource):
    @jwt_required
    def get(self):
        json_data = request.get_json()
        username = json_data["username"]

        user = User.query.filter_by(username=username).first()

        messages = []

        for message in user.authored_messages:
            message_dict = {
                "id": message.id,
                "room_id": message.room_id,
                "content": message.content,
                "is_system_message": message.is_system_message
            }

            messages.append(message_dict)

        return messages, HTTPStatus.OK

class GetUserContent(Resource):
    @jwt_required
    def get(self, username, content):
        user = User.query.filter_by(username=username).first()

        messages = []

        for message in user.authored_messages:
            if str(content) in message.content:
                message_dict = {
                    "message_id": message.id,
                    "room_id": message.room_id,
                    "content": message.content
                }

                messages.append(message_dict)

        return messages, HTTPStatus.OK

