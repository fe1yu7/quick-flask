from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_wtf import CSRFProtect

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
csrf_protect = CSRFProtect()
