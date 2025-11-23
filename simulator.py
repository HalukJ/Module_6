"""
Simple revenue/profit simulator that works with the existing MUDTPass database.

The simulator pulls users from the SQLite DB (see database.py) and estimates
monthly revenue, infrastructure cost, and profit for each plan based on the
current user mix and hours played.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from database import GamePassDatabase


@dataclass
class PlanProfit:
    plan: str
    users: int
    total_hours: float
    revenue: float
    cost: float
    profit: float


class SubscriptionSimulator:
    def __init__(
        self,
        db_path: Path | str = "mudtpass.db",
        infra_cost_per_hour: float = 0.20,
        pay_per_use_price: float = 0.40,
    ) -> None:
        self.db = GamePassDatabase(db_path)
        self.db.initialize()
        self.infra_cost_per_hour = infra_cost_per_hour
        self.pay_per_use_price = pay_per_use_price

    def _plan_prices(self) -> Dict[str, float]:
        catalog = self.db.get_plan_catalog()
        return {name: info["price"] for name, info in catalog["plans"].items()}

    def _users(self) -> List[Dict]:
        return self.db.get_all_users()

    def simulate(self) -> Tuple[Dict[str, PlanProfit], PlanProfit]:
        prices = self._plan_prices()
        users = self._users()

        plan_hours: Dict[str, float] = {plan: 0.0 for plan in prices}
        plan_counts: Dict[str, int] = {plan: 0 for plan in prices}

        for user in users:
            plan = user["plan"]
            hours = float(user["hours_per_month"])
            if plan not in prices:
                # Skip unknown plans to avoid skewing results.
                continue
            plan_counts[plan] += 1
            plan_hours[plan] += hours

        plan_results: Dict[str, PlanProfit] = {}
        for plan, price in prices.items():
            users_on_plan = plan_counts.get(plan, 0)
            hours_on_plan = plan_hours.get(plan, 0.0)
            revenue = price * users_on_plan
            cost = hours_on_plan * self.infra_cost_per_hour
            profit = revenue - cost
            plan_results[plan] = PlanProfit(
                plan=plan,
                users=users_on_plan,
                total_hours=hours_on_plan,
                revenue=round(revenue, 2),
                cost=round(cost, 2),
                profit=round(profit, 2),
            )

        total_hours = sum(plan_hours.values())
        baseline_revenue = total_hours * self.pay_per_use_price
        baseline_cost = total_hours * self.infra_cost_per_hour
        baseline_profit = baseline_revenue - baseline_cost
        baseline = PlanProfit(
            plan="Pay-per-use baseline",
            users=len(users),
            total_hours=round(total_hours, 2),
            revenue=round(baseline_revenue, 2),
            cost=round(baseline_cost, 2),
            profit=round(baseline_profit, 2),
        )

        return plan_results, baseline


if __name__ == "__main__":  # pragma: no cover
    simulator = SubscriptionSimulator()
    plan_results, baseline = simulator.simulate()

    print("=== Subscription profit simulation ===")
    for plan, metrics in plan_results.items():
        print(
            f"{plan:<10} users={metrics.users:<4} "
            f"revenue=${metrics.revenue:<8} cost=${metrics.cost:<8} profit=${metrics.profit:<8}"
        )
    print(
        f"\nBaseline (pay-per-use) profit: ${baseline.profit} "
        f"from {baseline.total_hours} total hours at ${simulator.pay_per_use_price}/hr"
    )
