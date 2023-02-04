from enum import Enum


class DataType(Enum):
    IMAGE = 0
    TEXT = 1
    TABULAR = 2
    AUDIO = 3
    VIDEO = 4
    MULTIMODAL_IMAGE_TEXT = 5