from dataclasses import dataclass, field

from bson import ObjectId

from backend.data_structs.PermissionType import PermissionType


@dataclass
class Permission:
    id: str = field(default=None)
    permission: PermissionType = field(default=PermissionType.EXECUTE)

    def to_dict(self):
        return {
            "id": str(self.id),
            "permission": self.permission.value,
        }

    def from_dict(self, permission_dict):
        self.id = permission_dict["id"]
        self.permission = PermissionType(permission_dict["permission"])
        return self

    @staticmethod
    def get_schema_flask():
        from flask_restx import fields
        return {
            "id": fields.String,
            "permission": fields.String,
        }
