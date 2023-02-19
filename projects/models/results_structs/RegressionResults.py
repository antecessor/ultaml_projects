import json
from dataclasses import dataclass, field


@dataclass
class RegressionResults:
    mse: float = field(default=None)
    rmse: float = field(default=None)
    mae: float = field(default=None)
    r2: float = field(default=None)
    train_loss: [float] = field(default=None)
    val_loss: [float] = field(default=None)
    train_time_seconds: float = field(default=None)
    test_time_seconds: float = field(default=None)

    # serlialize to json
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

