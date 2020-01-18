from flask_jwt_extended import get_current_user
from flask_restful import Resource
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy import or_, and_, desc, asc

from common.response import json_response
from ext import db
from common.jwt_utils import login_required
from resource.auth.models import Permission, Role, UserRole, RolePermission
from resource.auth.schema import RoleSchema, PermissionSchema


class UserRoleResource(Resource):
    @login_required
    def get(self, user):
        second_permission_alias = aliased(Permission, name="second_permission")
        third_permission_alias = aliased(Permission, name="third_permission")
        query_result = db.session.query(Permission, second_permission_alias, third_permission_alias)\
            .outerjoin(second_permission_alias, Permission.id == second_permission_alias.parent_id)\
            .outerjoin(third_permission_alias, second_permission_alias.id == third_permission_alias.parent_id)\
            .join(RolePermission, or_(RolePermission.permission_id == Permission.id,
                                      RolePermission.permission_id == second_permission_alias.id,
                                      RolePermission.permission_id == third_permission_alias.id))\
            .join(Role, and_(RolePermission.role_id == Role.id))\
            .join(UserRole, and_(Role.id == UserRole.role_id, UserRole.user_id == user.id))\
            .filter(Permission.parent_id.is_(None)).order_by(Permission.id, second_permission_alias.id, third_permission_alias.id)\
            .distinct()\
            .all()
        permission_schema = PermissionSchema(exclude=("child_permissions", ))
        data = list()
        first_temp, second_temp, third_temp = None, None, None
        for permission, second_permission, third_permission in query_result:
            first_permission_data = permission_schema.dump(permission).data
            second_permission_data = permission_schema.dump(second_permission).data
            third_permission_data = permission_schema.dump(third_permission).data
            if first_temp and first_temp["id"] == first_permission_data["id"]:
                if second_temp and second_temp["id"] == second_permission_data["id"]:
                    if third_temp and third_temp["id"] == third_permission_data["id"]:
                        pass
                    else:
                        data[-1]["children"][-1]["children"].append(third_permission_data)
                else:
                    second_permission_data["children"] = [third_permission_data, ] if third_permission_data else list()
                    data[-1]["children"].append(second_permission_data)
            else:
                first_permission_data["children"] = [second_permission_data, ] if second_permission_data else list()
                if third_permission_data:
                    second_permission_data["children"] = [third_permission_data, ]
                data.append(first_permission_data)
            first_temp = first_permission_data
            second_temp = second_permission_data
            third_temp = third_permission_data

        return json_response(data=data)
