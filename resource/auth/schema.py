from marshmallow import fields, post_dump

from ext import ma
from resource.auth.models import Role, RolePermission, Permission


class RoleSchema(ma.ModelSchema):
    id = fields.Integer()
    name = fields.String()
    role_permission = fields.Nested("RolePermissionSchema", many=True, exclude=("role", ))

    class Meta:
        model = Role
        fields = ("id", "name", "role_permission")

    @post_dump
    def format_middle_table(self, data):
        if data.get("role_permission"):
            data["permissions"] = list()
            for role_permission in data.get("role_permission", list()):
                permission = role_permission["permission"]
                if permission and not permission["parent_id"]:
                    data["permissions"].append(permission)
            if data.get("role_permission"):
                del data["role_permission"]


class PermissionSchema(ma.ModelSchema):
    id = fields.Integer()
    name = fields.String()
    action = fields.String()
    url = fields.String()
    parent_id = fields.Integer()
    child_permissions = fields.Nested('self', many=True, exclude=("parent_permission", ))
    # parent_permission = fields.Nested('self', exclude=("child_permissions", ))

    class Meta:
        model = Permission
        fields = ("id", "name", "parent_id", "child_permissions", "action", "url")


class RolePermissionSchema(ma.ModelSchema):
    id = fields.Integer()
    role = fields.Nested(RoleSchema)
    permission = fields.Nested(PermissionSchema)

    class Meta:
        model = RolePermission
        fields = ("id", "permission", "role")

