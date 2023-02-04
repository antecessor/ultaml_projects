from abc import ABC, abstractmethod

from backend.data_structs.DataType import DataType


class BaseData(ABC):

    def __init__(self, type=DataType.TABULAR) -> None:
        super().__init__()
        self.type: DataType = type

    @abstractmethod
    def load(self, path):
        raise NotImplementedError("Please implement this method")

    @abstractmethod
    def save(self, path):
        raise NotImplementedError("Please implement this method")
