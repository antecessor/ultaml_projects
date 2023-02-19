import dataclasses
import json
from dataclasses import dataclass, field


@dataclass
class TrainingConfig:
    data_path: str = field(default="")
    max_depth: int = field(default=3)
    eta: float = field(default=0.1)
    objective: str = field(default="multi:softmax")
    num_class: int = field(default=None)
    validation: str = field(default="hold_out_20")

    def to_arguments(self) -> str:
        args = []
        for item in dataclasses.fields(self):
            value = getattr(self, item.name)
            if value is not None:
                args.append(f"--{item.name}={value}")

        return " ".join(args)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
