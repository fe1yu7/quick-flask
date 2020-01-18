from flask import Blueprint
from flask_restful import Api

from .views import UserRoleResource

blueprint = Blueprint("auth", __name__)
api = Api(blueprint)

api.add_resource(UserRoleResource, "/user/role")