from functools import wraps

from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, create_access_token, create_refresh_token, get_current_user
from flask_jwt_extended.exceptions import NoAuthorizationError

from common.response import json_response
from ext import jwt, db
from resource.user.models import User
from resource.auth.models import UserRole, Role, Permission, RolePermission


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.filter_by(id=identity["id"], is_able=1).first()


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError as e:
            _ = e
            return json_response(message="not authorization", status=401)
        user = get_current_user()
        if not user:
            return json_response(message="account is disabled", status=403)
        return fn(user=user, *args, **kwargs)

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


def permission_required(description):
    def wrapper(fn):
        def _wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except NoAuthorizationError as e:
                _ = e
                return json_response(message="not authorization", status=401)
            user = get_current_user()
            if not user:
                return json_response(message="account is disabled", status=403)

            second_permission_alias = aliased(Permission, name="second_permission")
            third_permission_alias = aliased(Permission, name="third_permission")
            permission = db.session.query(Permission.id) \
                .outerjoin(second_permission_alias, Permission.id == second_permission_alias.parent_id) \
                .outerjoin(third_permission_alias, second_permission_alias.id == third_permission_alias.parent_id) \
                .join(RolePermission, or_(RolePermission.permission_id == Permission.id,
                                          RolePermission.permission_id == second_permission_alias.id,
                                          RolePermission.permission_id == third_permission_alias.id)) \
                .join(Role, and_(RolePermission.role_id == Role.id)) \
                .join(UserRole, and_(Role.id == UserRole.role_id, UserRole.user_id == user.id)) \
                .filter(Permission.parent_id.is_(None), or_(Permission.description == description,
                                                            second_permission_alias.description == description,
                                                            third_permission_alias.description == description))\
                .order_by(Permission.id, second_permission_alias.id, third_permission_alias.id) \
                .first()
            if permission:
                return fn(user, *args, **kwargs)
            else:
                return json_response(message='permission denied', status=401)
        return _wrapper
    return wrapper
