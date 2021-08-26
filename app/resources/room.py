from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import *

class OneRoom(Resource):
    @jwt_required
    def get(self):
        json_data = request.get_json()
        room_id = json_data["room_id"]
        room = Room.query.filter_by(id=room_id).first()
        if room:
            return room.get_data(), HTTPStatus.OK
        else:
            return {"message": "Room not found"}, HTTPStatus.NOT_FOUND

    @jwt_required
    def put(self):
        json_data = request.get_json()
        room_id = json_data["room_id"]
        user = User.query.filter_by(id=get_jwt_identity()).first()
        room = Room.query.filter_by(id=room_id).first()
        if user.is_admin and not room.id == 1:
            if room:
                db.session.delete(room)
                db.session.commit()
                return {f"Successfully deleted {room.room_name}"}, HTTPStatus.OK
            else:
                return {"message": "Room not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED

    @jwt_required
    def patch(self):
        json_data = request.get_json()
        room_id = json_data["room_id"]
        new_room_name = json_data["new_room_name"]
        user = User.query.filter_by(id=get_jwt_identity()).first()
        room = Room.query.filter_by(id=room_id).first()
        if room.owner == user.username or user.is_admin and not room.id == 1:
            if not Room.query.filter_by(room_name=new_room_name).first():
                room.room_name = new_room_name
                db.session.commit()
                return {"message": f"Successfully changed room name to {new_room_name}"}, HTTPStatus.OK
            else:
                return {"message": "Room already exists"}, HTTPStatus.BAD_REQUEST
        else:
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED

class ALlRooms(Resource):
    @jwt_required
    def get(self):
        rooms = [room.get_data() for room in Room.query.all()]
        return rooms, HTTPStatus.OK

    @jwt_required
    def put(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.is_admin:
            for room in Room.query.all():
                if not room.id == 1:
                    db.session.delete(room)
            db.session.commit()
            return {"message": "Successfully deleted all rooms"}, HTTPStatus.OK
        else:
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED




