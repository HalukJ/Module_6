from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SubscriptionPlan:
    """
    Represents a subscription plan for NovaPlay Pass.
    """
    name: str
    duration_months: int
    base_price: float        # fixed price per duration
    included_hours: float    # hours included in the base price
    extra_hour_price: float  # price per extra hour above included_hours


class SubscriptionCatalog:
    """
    Holds all available subscription plans and pay-per-use info.
    """

    def __init__(self) -> None:
        # You can later tweak these numbers to experiment with pricing.
        self.plans: Dict[str, SubscriptionPlan] = {
            "Monthly": SubscriptionPlan(
                name="Monthly",
                duration_months=1,
                base_price=15.0,
                included_hours=40.0,
                extra_hour_price=0.50
            ),
            "Half-Year": SubscriptionPlan(
                name="Half-Year",
                duration_months=6,
                base_price=70.0,
                included_hours=250.0,
                extra_hour_price=0.40
            ),
            "Yearly": SubscriptionPlan(
                name="Yearly",
                duration_months=12,
                base_price=120.0,
                included_hours=600.0,
                extra_hour_price=0.30
            ),
        }

        # Users without any subscription pay per hour.
        self.pay_per_use_price: float = 0.60

    def get_all_plans(self) -> List[SubscriptionPlan]:
        return list(self.plans.values())

    def get_plan(self, name: str) -> SubscriptionPlan:
        return self.plans[name]