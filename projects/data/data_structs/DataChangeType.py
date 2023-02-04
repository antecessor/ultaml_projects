from enum import Enum


class DataChangeType(Enum):
    """Enum for data change type."""
    ADD = 0
    REMOVE = 1
    MODIFY = 2
    COMBINE = 3