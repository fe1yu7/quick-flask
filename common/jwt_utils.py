from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, create_access_token, create_refresh_token
from flask_jwt_extended.exceptions import NoAuthorizationError

from common.response import json_response
from ext import jwt, db
from resource.user.models import User


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(identity["id"])


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError as e:
            _ = e
            return json_response(status=403)
        identity = get_jwt_identity()
        user = db.session.query(User.id).filter_by(id=identity["id"], is_able=1).first()
        if not user:
            return json_response(message="account is disabled", status=403)
        return fn(*args, **kwargs)

    return wrapper


def get_access_token(user):
    """
    create token
    :param user: User object
    :return:
    """
    if not isinstance(user, User):
        raise Exception("place input correct param")
    identity = {
        "id": user.id,
        "phone": user.phone
    }
    return create_access_token(identity=identity)
