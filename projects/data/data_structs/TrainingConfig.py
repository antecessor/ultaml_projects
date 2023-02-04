from dataclasses import dataclass, field


@dataclass
class TrainingConfig:
    train_data_path: str = field(default=None)
    test_data_path: str = field(default=None)
    batch_size: int = field(default=32)
    epochs: int = field(default=10)
    learning_rate: float = field(default=0.001)
    optimizer: str = field(default="Adam")
    loss: str = field(default="categorical_crossentropy")
    metrics: list = field(default_factory=lambda: ["accuracy"])
    validation_split: float = field(default=0.2)
    shuffle: bool = field(default=False)

    def to_dict(self):
        return {
            "train_data_path": self.train_data_path,
            "test_data_path": self.test_data_path,
            "batch_size": self.batch_size,
            "epochs": self.epochs,
            "learning_rate": self.learning_rate,
            "optimizer": self.optimizer,
            "loss": self.loss,
            "metrics": self.metrics,
            "validation_split": self.validation_split,
            "shuffle": self.shuffle,

        }

    @staticmethod
    def from_dict(training_config_dict):
        training_config = TrainingConfig()
        if "train_data_path" in training_config_dict:
            training_config.train_data_path = training_config_dict["train_data_path"]
        if "test_data_path" in training_config_dict:
            training_config.test_data_path = training_config_dict["test_data_path"]
        if "batch_size" in training_config_dict:
            training_config.batch_size = training_config_dict["batch_size"]
        if "epochs" in training_config_dict:
            training_config.epochs = training_config_dict["epochs"]
        if "learning_rate" in training_config_dict:
            training_config.learning_rate = training_config_dict["learning_rate"]
        if "optimizer" in training_config_dict:
            training_config.optimizer = training_config_dict["optimizer"]
        if "loss" in training_config_dict:
            training_config.loss = training_config_dict["loss"]
        if "metrics" in training_config_dict:
            training_config.metrics = training_config_dict["metrics"]
        if "validation_split" in training_config_dict:
            training_config.validation_split = training_config_dict["validation_split"]
        if "shuffle" in training_config_dict:
            training_config.shuffle = training_config_dict["shuffle"]
        if "callbacks" in training_config_dict:
            training_config.callbacks = training_config_dict["callbacks"]
        if "class_weight" in training_config_dict:
            training_config.class_weight = training_config_dict["class_weight"]
        return training_config
