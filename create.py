from flask import Flask
from app.models import *
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def main():
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()