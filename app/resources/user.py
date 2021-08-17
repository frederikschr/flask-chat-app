from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User

class GetMyPassword(Resource):
    @jwt_required
    def get(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        return {"password": user.password}

class GetAllUsers(Resource):
    @jwt_required
    def get(self):
        users = []
        for user in User.query.all():
            user_dict = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "owned_rooms": [room.room_name for room in user.owned_rooms],
                "rooms": [room.room_name for room in user.rooms]
            }

            users.append(user_dict)

        return users

class GetOneUser(Resource):
    @jwt_required
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {"id": user.id, "username": user.username, "email": user.email, "owned_rooms": [room.room_name for room in user.owned_rooms], "rooms": [room.room_name for room in user.rooms]} if user else {"message": "User not found"}

class GetAllUserMessages(Resource):
    @jwt_required
    def get(self):
        json_data = request.get_json()
        username = json_data["username"]

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}

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

        if not user:
            return {"message": "User not found"}

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
