from dataclasses import dataclass, field

from backend.data_structs.SubscriptionLevel import SubscriptionLevel


@dataclass
class Limits:
    storage_limit: int = field(default=50)  # 50 MB
    storage_used: int = field(default=0)
    subscription: SubscriptionLevel = field(default=SubscriptionLevel.Basic)

    def to_dict(self):
        return {
            "storage_limit": self.storage_limit,
            "storage_used": self.storage_used,
            "subscription": self.subscription.value,
        }

    @staticmethod
    def from_dict(limits_dict):
        storage_limit = limits_dict["storage_limit"]
        storage_used = limits_dict["storage_used"]
        if "subscription" in limits_dict:
            subscription = SubscriptionLevel(limits_dict["subscription"])
        else:
            subscription = SubscriptionLevel.Basic
        return Limits(storage_limit, storage_used, subscription)
