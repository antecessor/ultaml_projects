import json
from dataclasses import dataclass, field
import datetime

from projects.data.data_structs.DownstreamTask import DownstreamTask
from projects.data.data_structs.SubscriptionLevel import SubscriptionLevel
from projects.data.data_structs.TrainingConfig import TrainingConfig


@dataclass
class Model:
    id: str = field(default=None)
    name: str = field(default=None)
    version: int = field(default=0)
    parent_version: int = field(default=0)
    base: str = field(default="")  # id for base model
    description: str = field(default=None)
    thumbnail_path: str = field(default=None)
    path: str = field(default=None) #s3 path or URL of the model weight file
    code_path: str = field(default=None) #public git repository
    downstream_task: DownstreamTask = field(
        default_factory=lambda: DownstreamTask.CLASSIFICATION)
    subscription_level: SubscriptionLevel = field(
        default_factory=lambda: SubscriptionLevel.Basic)
    training_config: any = field(
        default_factory=lambda: TrainingConfig().to_dict())
    results: dict = field(default_factory=dict)
    deleted: bool = field(default=False)
    uploading_progress: int = field(default=0)
    created_at: datetime.datetime = field(default=datetime.datetime.now())
    updated_at: datetime.datetime = field(default=datetime.datetime.now())

    def generate_path(self, email: str):
        # probably: email_base_name_version -> unique for that user and project
        self.path = f"{email}_{self.name}_{self.version}"
        return self.path

    def to_dict(self, id_as_str=True):
        model = {
            "name": self.name,
            "version": self.version,
            "parent_version": self.parent_version,
            "base": self.base,
            "description": self.description,
            "thumbnail_path": self.thumbnail_path,
            "path": self.path,
            "code_path": self.code_path,
            "downstream_task": self.downstream_task.value,
            "subscription_level": self.subscription_level.value,
            "results": self.results,
            "deleted": self.deleted,
            "uploading_progress": self.uploading_progress,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            model["training_config"]= self.training_config.to_json()
        except:
            model["training_config"] = self.training_config

        if self.id:
            model["_id"] = str(self.id) if id_as_str else self.id
        return model

    @staticmethod
    def from_dict_all_string(model_dict):
        model = Model()
        if model_dict is None:
            return model
        if "_id" in model_dict:
            model.id = model_dict["_id"]
        if "name" in model_dict:
            model.name = model_dict["name"]
        if "version" in model_dict:
            model.version = model_dict["version"]
        if "parent_version" in model_dict:
            model.parent_version = model_dict["parent_version"]
        if "base" in model_dict:
            model.base = model_dict["base"]
        if "description" in model_dict:
            model.description = model_dict["description"]
        if "thumbnail_path" in model_dict:
            model.thumbnail_path = model_dict["thumbnail_path"]
        if "path" in model_dict:
            model.path = model_dict["path"]
        if "code_path" in model_dict:
            model.code_path = model_dict["code_path"]
        if "downstream_task" in model_dict:
            model.downstream_task = DownstreamTask(model_dict["downstream_task"])
        if "subscription_level" in model_dict:
            model.subscription_level = SubscriptionLevel(
                model_dict["subscription_level"])
        if "training_config" in model_dict:
            try:
                model.training_config = json.loads(model_dict["training_config"])
            except:
                model.training_config = model_dict["training_config"]
        if "results" in model_dict:
            try:
                model.results = json.loads(model_dict["results"])
            except:
                model.results = model_dict["results"]
        if "deleted" in model_dict:
            model.deleted = model_dict["deleted"]
        if "uploading_progress" in model_dict:
            model.uploading_progress = int(model_dict["uploading_progress"])
        if "created_at" in model_dict:
            model.created_at = datetime.datetime.fromisoformat(model_dict["created_at"])
        if "updated_at" in model_dict:
            model.updated_at = datetime.datetime.fromisoformat(model_dict["updated_at"])
        return model

    @staticmethod
    def get_schema_flask():
        from flask_restx import fields
        return {
            "name": fields.String,
            "version": fields.Integer,
            "parent_version": fields.Integer,
            "base": fields.String,
            "description": fields.String,
            "thumbnail_path": fields.String,
            "path": fields.String,
            "code_path": fields.String,
            "downstream_task": fields.String,
            "subscription_level": fields.Integer,
            "training_config": fields.Raw,
            "result": fields.Raw,
            "deleted": fields.Boolean,
            # optional
            "uploading_progress": fields.Integer,
            "created_at": fields.String,
            "updated_at": fields.String
        }
