from flask import Blueprint
from flask_restful import Api

from resource.user.views import UserResource, UserPhoneResource, UserLoginResource


blueprint = Blueprint("user", __name__)
api = Api(blueprint)

api.add_resource(UserResource, "")
api.add_resource(UserPhoneResource, "/phone")
api.add_resource(UserLoginResource, "/login")
