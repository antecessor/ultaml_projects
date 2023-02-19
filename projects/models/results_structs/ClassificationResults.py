from dataclasses import dataclass, field
from typing import Union

import numpy as np


@dataclass
class ClassificationResults:
    accuracy: float = field(default=None)
    precision: float = field(default=None)
    recall: float = field(default=None)
    f1: float = field(default=None)
    auc: float = field(default=None)
    confusion_matrix: []= field(default=None)
    feature_importance: list = field(default=None)
    train_loss: [float] = field(default=None)
    val_loss: [float] = field(default=None)
    train_time_seconds: float = field(default=None)
    test_time_seconds: float = field(default=None)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
