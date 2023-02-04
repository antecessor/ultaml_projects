from enum import Enum


class DownstreamTask(Enum):
    CLASSIFICATION = 0
    CLUSTERING = 1
    REGRESSION = 2
    OBJECT_DETECTION = 3
    SEGMENTATION = 4
    QUESTION_ANSWERING = 5
    ENTITY_EXTRACTION = 6
    # OCR = 7
    # RANKING = 8

    @staticmethod
    def get_by_name(name):
        return DownstreamTask[name.upper()]
