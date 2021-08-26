from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from app.models import *

class OneMessage(Resource):
    @jwt_required
    def get(self):
        json_data = request.get_json()
        content = json_data['content']
        messages = [message.get_data() for message in Message.query.all() if content in message.content]
        return messages, HTTPStatus.OK

class ALlMessages(Resource):
    @jwt_required
    def get(self):
        json_data = request.get_json()
        user_id = json_data["user_id"]
        content = json_data["content"]
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND
        messages = [message.get_data() for message in user.messages if content in message.content]
        return messages, HTTPStatus.OK








