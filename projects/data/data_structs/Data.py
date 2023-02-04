from dataclasses import dataclass, field
import datetime
from typing import List

from backend.data_structs.DownstreamTask import DownstreamTask
from backend.data_structs.MetaData import MetaData
from backend.data_structs.SubscriptionLevel import SubscriptionLevel


@dataclass
class Data:
    id: str = field(default=None)
    name: str = field(default=None)
    version: str = field(default="0.0.0")
    parent_version: str = field(default="0.0.0")
    description: str = field(default=None)
    thumbnail_path: str = field(default=None)

    path: str = field(default=None)
    downstream_task: DownstreamTask = field(
        default_factory=lambda: DownstreamTask.CLASSIFICATION)
    annotated: bool = field(default=False)
    meta_data: MetaData = field(default_factory=lambda: MetaData())
    children: List[dict] = field(default_factory=lambda: [])

    subscription_level: SubscriptionLevel = field(
        default_factory=lambda: SubscriptionLevel.Basic)

    deleted: bool = field(default=False)
    uploading_progress: int = field(default=0)
    created_at: datetime.datetime = field(default=datetime.datetime.now())
    updated_at: datetime.datetime = field(default=datetime.datetime.now())

    def generate_path(self, email: str):
        #: probably: email_name_version -> unique for that user
        self.path = f"{email}_{self.name}_{self.version}"
        return self.path

    def to_dict(self, id_as_str=True):
        data = {
            "name": self.name,
            "version": self.version,
            "parent_version": self.parent_version,
            "description": self.description,
            "thumbnail_path": self.thumbnail_path,
            "path": self.path,
            "downstream_task": self.downstream_task.value,
            "annotated": self.annotated,
            "meta_data": self.meta_data.to_dict(),
            "children": self.children,
            "subscription_level": self.subscription_level.value,
            "deleted": self.deleted,
            "uploading_progress": self.uploading_progress,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        if self.id:
            data["_id"] = str(self.id) if id_as_str else self.id

        return data

    @staticmethod
    def from_dict_all_string(data_dict):
        data = Data()
        # if _id exists, then it is a valid data
        if "_id" in data_dict:
            data.id = data_dict["_id"]
        if "name" in data_dict:
            data.name = data_dict["name"]
        if "version" in data_dict:
            data.version = data_dict["version"]
        if "parent_version" in data_dict:
            data.parent_version = data_dict["parent_version"]
        if "description" in data_dict:
            data.description = data_dict["description"]
        if "thumbnail_path" in data_dict:
            data.thumbnail_path = data_dict["thumbnail_path"]
        if "path" in data_dict:
            data.path = data_dict["path"]
        if "downstream_task" in data_dict:
            data.downstream_task = DownstreamTask(data_dict["downstream_task"])
        if "annotated" in data_dict:
            data.annotated = bool(data_dict["annotated"])
        if "meta_data" in data_dict:
            data.meta_data = MetaData.from_dict(data_dict["meta_data"])
        if "children" in data_dict:
            data.children = data_dict["children"]
        if "subscription_level" in data_dict:
            data.subscription_level = SubscriptionLevel(data_dict["subscription_level"])
        if "deleted" in data_dict:
            data.deleted = bool(data_dict["deleted"])
        if "uploading_progress" in data_dict:
            data.uploading_progress = int(data_dict["uploading_progress"])
        if "created_at" in data_dict:
            data.created_at = datetime.datetime.fromisoformat(data_dict["created_at"])
        if "updated_at" in data_dict:
            data.updated_at = datetime.datetime.fromisoformat(data_dict["updated_at"])
        return data

    @staticmethod
    def get_schema_flask():
        from flask_restx import fields
        return {
            "name": fields.String,
            "version": fields.Integer,
            "parent_version": fields.Integer,
            "description": fields.String,
            "thumbnail_path": fields.String,
            "path": fields.String,
            "downstream_task": fields.String,
            "annotated": fields.Boolean,
            "meta_data": MetaData.get_schema_flask(),
            "children": fields.Raw,
            "subscription_level": fields.Integer,
            "deleted": fields.Boolean,
            # optional
            "uploading_progress": fields.Integer,
            "created_at": fields.String,
            "updated_at": fields.String
        }
