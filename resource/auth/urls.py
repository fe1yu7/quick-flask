from flask import Blueprint
from flask_restful import Api

from resource.auth.views import *

blueprint = Blueprint("auth", __name__)
api = Api(blueprint)

