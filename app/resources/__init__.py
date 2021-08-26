from flask_jwt_extended import JWTManager
from .token import *
from .user import *
from .message import *
from .room import *

jwt = JWTManager()