from enum import Enum


class PermissionType(Enum):
    """Enum for permission type."""
    READ = 0
    WRITE = 1
    EXECUTE = 2
