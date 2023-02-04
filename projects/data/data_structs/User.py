from dataclasses import dataclass, field
import datetime
from typing import List

from backend.data_structs.Limits import Limits
from backend.data_structs.Permission import Permission
from backend.data_structs.PermissionType import PermissionType


@dataclass
class User:
    id: str = field(default=None)
    email: str = field(default=None)
    model_perm: List[Permission] = field(default_factory=lambda: [])
    data_perm: List[Permission] = field(default_factory=lambda: [])
    limits: Limits = field(default_factory=lambda: Limits())
    created_at: datetime.datetime = field(default=datetime.datetime.now())
    updated_at: datetime.datetime = field(default=datetime.datetime.now())

    def add_data_perm(self, data_id: str,
                      permission: PermissionType = PermissionType.EXECUTE):
        self.data_perm.append(Permission(data_id, permission))

    def add_model_perm(self, model_id: str,
                       permission: PermissionType = PermissionType.EXECUTE):
        self.model_perm.append(Permission(model_id, permission))

    def delete_perm(self, perm_id: str):
        for perm in self.model_perm:
            if perm.id == perm_id:
                self.model_perm.remove(perm)
                return
        for perm in self.data_perm:
            if perm.id == perm_id:
                self.data_perm.remove(perm)
                return

    def to_dict(self, id_as_str: bool = True):
        user =  {
            "email": self.email,
            "model_perm": [perm.to_dict() for perm in self.model_perm],
            "data_perm": [perm.to_dict() for perm in self.data_perm],
            "limits": self.limits.to_dict(),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        if self.id:
            user["_id"] = str(self.id) if id_as_str else self.id
        return user

    @staticmethod
    def from_dict_all_string(data_dict):
        user = User()
        if "_id" in data_dict:
            user.id = data_dict["_id"]
        if "email" in data_dict:
            user.email = data_dict["email"]
        if "model_perm" in data_dict:
            user.model_perm = [Permission().from_dict(perm) for perm in
                               data_dict["model_perm"]]
        if "data_perm" in data_dict:
            user.data_perm = [Permission().from_dict(perm) for perm in
                              data_dict["data_perm"]]
        if "limits" in data_dict:
            user.limits = Limits().from_dict(data_dict["limits"])
        else:
            user.limits = Limits()

        if "created_at" in data_dict:
            user.created_at = datetime.datetime.fromisoformat(data_dict["created_at"])
        if "updated_at" in data_dict:
            user.updated_at = datetime.datetime.fromisoformat(data_dict["updated_at"])
        return user

    @staticmethod
    def get_schema_flask():
        from flask_restx import fields
        return {
            "id": fields.String,
            "email": fields.String,
            "model_perm": fields.Raw,
            "data_perm": fields.Raw,
            "limits": fields.Raw,
        }




