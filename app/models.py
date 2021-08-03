from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
DB_NAME = "database.db"

room_members = db.Table("room_members",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("room_id", db.Integer, db.ForeignKey("room.id"))
                        )

message_receivers = db.Table("message_receivers",
                             db.Column("message_id", db.Integer, db.ForeignKey("message.id")),
                             db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                             )

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    authored_messages = db.relationship('Message')
    owned_rooms = db.relationship('Room')
    rooms = db.relationship('Room', secondary=room_members, backref=db.backref('members', lazy='dynamic'))

class Room(db.Model):
    __tablename__ = "room"

    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100))
    owner = db.Column(db.String(80), db.ForeignKey('user.username'))
    messages = db.relationship('Message')

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    author = db.Column(db.String(80), db.ForeignKey('user.username'))
    content = db.Column(db.String(500))
    receivers = db.relationship('User', secondary=message_receivers, backref=db.backref('messages', lazy='dynamic'))
    is_system_message = db.Column(db.Boolean, default=False)
