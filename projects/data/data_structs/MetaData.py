from dataclasses import dataclass, field

from projects.data.data_structs.DataType import DataType


@dataclass
class MetaData:
    data_type: DataType = field(default=DataType.IMAGE)
    data_format: str = field(default=None)

    def to_dict(self):
        return {
            "data_type": self.data_type.value,
            "data_format": self.data_format
        }

    @staticmethod
    def from_dict(meta_data_dict):
        meta_data = MetaData()
        if "data_type" in meta_data_dict:
            meta_data.data_type = DataType(meta_data_dict["data_type"])
        if "data_format" in meta_data_dict:
            meta_data.data_format = meta_data_dict["data_format"]
        return meta_data

    @staticmethod
    def get_schema_flask():
        from flask_restx import fields
        return {
            "data_type": fields.String,
            "data_format": fields.String
        }
