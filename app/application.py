from flask_socketio import SocketIO, emit, send, join_room, leave_room
from app import app

socketio = SocketIO(app)

@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})

