from marshmallow import fields, Schema

from resource.user.models import User, UserInfo


class UserSchema(Schema):
    phone = fields.String()
    nickname = fields.String()

    class Meta:
        model = User


class UserInfoSchema(Schema):
    unique_id = fields.String()
    birth_date = fields.String()

    class Meta:
        model = UserInfo

    """
    数据格式再转换
    @post_dump
    def decimal_to_float(self, data):
        data = {k: float(v) if isinstance(v, Decimal) else v for k, v in data.items()}
        return data
    """