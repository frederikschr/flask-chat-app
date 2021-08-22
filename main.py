from app import create_app

socketio, app = create_app()

if __name__ == '__main__':
    with app.app_context():
        socketio.run(app, debug=True)




