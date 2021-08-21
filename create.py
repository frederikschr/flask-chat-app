from flask import Flask
from app.models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://opmjebsqhswdqf:eedacb5d20c1dad296b08961bbcf9d586436914024eb9edb767726cde2d56f08@ec2-54-155-254-112.eu-west-1.compute.amazonaws.com:5432/d8g0ng33rj7fl2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()