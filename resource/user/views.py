
from flask_restful import Resource
from flask_jwt_extended import get_current_user
from flask_apispec import use_kwargs
from marshmallow import fields

from ext import db
from common.response import json_response
from common.utils import valid_phone, valid_password
from common.auth_utils import login_required, get_access_token, permission_required
from resource.user.models import User
from resource.user.schema import UserSchema


class UserResource(Resource):
    @use_kwargs({
        "phone": fields.String(required=True),
        "nickname": fields.String(required=True),
        "password": fields.String(required=True),
    }, locations=("json", ))
    def post(self, **kwargs):
        exist_user = db.session.query(User.id).filter_by(phone=kwargs["phone"]).first()
        if exist_user:
            return json_response(message="user exists")
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return json_response(message="user create success", data={
            "access_token": get_access_token(user)
        })


class UserPhoneResource(Resource):
    @login_required
    @use_kwargs({
        "phone": fields.String(required=True, validate=valid_phone)
    })
    def put(self, phone):

        current_user = get_current_user()

        user_phone = db.session.query(User.phone).filter(
            User.phone == phone
        ).first()
        if user_phone:
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


class UserLoginResource(Resource):
    @use_kwargs({
        "phone": fields.String(required=True, validate=valid_phone),
        "password": fields.String(required=True, validate=valid_password)
    })
    def post(self, phone, password):
        user = db.session.query(User).filter(User.phone == phone, User.password == password).first()
        if not user:
            return json_response(message='username or password error', status=403)

        return json_response(data={
            "access_token": get_access_token(user)
        })

    @permission_required('会员中心')
    def get(self):
        return 'xxx'