
from flask_restful import Resource
from flask_jwt_extended import get_current_user
from flask_apispec import use_kwargs
from marshmallow import fields

from ext import db
from common.response import json_response
from common.utils import valid_phone
from common.jwt_utils import login_required, get_access_token
from resource.user.models import User
from resource.user.schema import UserSchema


class UserResource(Resource):
    @use_kwargs({
        "phone": fields.String(required=True),
        "nickname": fields.String(required=True),
        "password": fields.String(required=True),
    }, locations=("json", ))
    def post(self, **kwargs):
        """"""
        exist_user = User.query.filter_by(phone=kwargs.get("phone")).first()
        if exist_user:
            return {
                "msg": "用户已经存在"
            }
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return {
            "msg": "用户创建成功",
            "access_token": get_access_token(user.id)
        }

    @staticmethod
    def get():
        user_paginate = User.query.paginate()
        user_schema = UserSchema(many=True)
        data = user_schema.dump(user_paginate.items).data
        return json_response(data=data, paginate=user_paginate, status=404)


class UserPhoneResource(Resource):
    @use_kwargs({
        "phone": fields.String(required=True, validate=valid_phone)
    })
    @login_required
    def put(self, phone):

        current_user = get_current_user()

        user_phone = db.session.query(User.phone).filter(
            User.phone == phone
        ).first()
        if user_phone and user_phone.phone != current_user.phone:
            return json_response(message="exists phone", status=403)

        try:
            current_user.phone = phone
            db.session.add(current_user)
            db.session.commit()
        except Exception as e:
            _ = e
            db.session.rollback()
            return json_response(message="bind phone failed")
        else:
            return json_response(message="bind phone success")
