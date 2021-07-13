from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
DB_NAME = "database.db"

room_members = db.Table("room_members",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("room_id", db.Integer, db.ForeignKey("room.id"))
                        )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    rooms = db.relationship('Room', secondary=room_members, backref=db.backref('members', lazy='dynamic'))

class Room(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100))
    owner = db.Column(db.String(10))


