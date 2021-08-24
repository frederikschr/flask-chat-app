from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import *
from werkzeug.security import check_password_hash, generate_password_hash

class OneUser(Resource):
    @jwt_required
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {"id": user.id, "username": user.username, "email": user.email,
                "owned_rooms": [room.room_name for room in user.owned_rooms],
                "rooms": [room.room_name for room in user.rooms]} if user else {"message": "User not found"}

    @jwt_required
    def put(self, id):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        user_delete = User.query.filter_by(id=id).first()
        if user.is_admin:
            if user_delete:
                db.session.delete()
                db.session.commit()
                return {"message": f"Successfully deleted {user.username}"}, HTTPStatus.OK
            else:
                return {"message": "User not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED

class AllUsers(Resource):
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
        return users, HTTPStatus.OK

    @jwt_required
    def put(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.is_admin:
            for user in User.query.all():
                db.session.delete(user)
            db.session.commit()
            return {"message": "Successfully deleted all users"}, HTTPStatus.OK
        else:
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED

class MyUser(Resource):
    @jwt_required
    def get(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        return user.get_data(), HTTPStatus.OK

    @jwt_required
    def patch(self):
        json_data = request.get_json()
        password = json_data["password"]
        new_password = json_data["new_password"]
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if check_password_hash(user.password, password):
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return {"message": "Successfully updated password"}, HTTPStatus.OK
        else:
            return {"message": "Password is incorrect"}, HTTPStatus.UNAUTHORIZED

    @jwt_required
    def put(self):
        json_data = request.get_json()
        password = json_data["password"]
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if check_password_hash(user.password, password):
            db.session.delete(user)
            db.session.commit()
            return {"message": "Successfully deleted account"}, HTTPStatus.OK
        else:
            return {"message": "Password is incorrect"}, HTTPStatus.UNAUTHORIZED















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
