import re

from marshmallow import fields
from flask_apispec import use_kwargs
from flask_restful import Resource


def valid_phone(phone):
    phone_rule = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
    return True if re.match(phone_rule, phone) else False


class TestResource(Resource):
    @use_kwargs({
        "phone": fields.String(required=True, validate=valid_phone),
        "phone_code": fields.String(required=True, validate=lambda phone_code: True if len(phone_code) == 6 else False)
    }, locations="querystring")
    def post(self):
        pass
