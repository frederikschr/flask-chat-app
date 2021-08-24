from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import create_access_token
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