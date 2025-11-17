from typing import Dict, Any

from database_manager import DatabaseManager
from subscription_plans import SubscriptionCatalog, SubscriptionPlan


class SubscriptionSimulator:
    """
    Uses historical usage data to estimate revenue, cost and profit
    for each subscription plan.
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        catalog: SubscriptionCatalog,
        infra_cost_per_hour: float = 0.20
    ) -> None:
        self.db_manager = db_manager
        self.catalog = catalog
        # Infrastructure cost per gaming hour (servers, bandwidth, etc.)
        self.infra_cost_per_hour = infra_cost_per_hour

    def _revenue_for_plan(self, plan: SubscriptionPlan, hours: float) -> float:
        """
        Revenue from one user if they are on a given subscription plan.
        """
        if hours <= plan.included_hours:
            return plan.base_price
        extra_hours = hours - plan.included_hours
        return plan.base_price + extra_hours * plan.extra_hour_price

    def _cost_for_usage(self, hours: float) -> float:
        """
        Cost of serving a given user for a given number of hours.
        """
        return hours * self.infra_cost_per_hour

    def _revenue_pay_per_use(self, hours: float) -> float:
        """
        Revenue from one user that has no subscription (pay-per-use).
        """
        return hours * self.catalog.pay_per_use_price

    def simulate_all_plans(self) -> Dict[str, Dict[str, Any]]:
        """
        For each subscription plan, assume all users are on that plan
        and compute total revenue, cost and profit.
        Also compute a baseline pay-per-use scenario.
        """
        users = self.db_manager.fetch_all_users()
        n_users = len(users)

        # Baseline: everyone is pay-per-use
        baseline_revenue = 0.0
        baseline_cost = 0.0
        for u in users:
            h = u["monthly_hours"]
            baseline_revenue += self._revenue_pay_per_use(h)
            baseline_cost += self._cost_for_usage(h)

        baseline_profit = baseline_revenue - baseline_cost

        results: Dict[str, Dict[str, Any]] = {
            "Pay-Per-Use (baseline)": {
                "total_revenue": baseline_revenue,
                "total_cost": baseline_cost,
                "total_profit": baseline_profit,
                "avg_profit_per_user": baseline_profit / n_users if n_users > 0 else 0.0,
            }
        }

        # Now simulate each subscription plan
        for plan in self.catalog.get_all_plans():
            total_revenue = 0.0
            total_cost = 0.0

            for u in users:
                hours = u["monthly_hours"]
                total_revenue += self._revenue_for_plan(plan, hours)
                total_cost += self._cost_for_usage(hours)

            total_profit = total_revenue - total_cost

            results[plan.name] = {
                "total_revenue": total_revenue,
                "total_cost": total_cost,
                "total_profit": total_profit,
                "avg_profit_per_user": total_profit / n_users if n_users > 0 else 0.0,
            }

        return results

    def best_plan_by_profit(self) -> str:
        """
        Returns the name of the plan with the highest total profit.
        """
        results = self.simulate_all_plans()
        # Ignore current_plan from DB here; we compare "what if everyone had this plan?"
        best_name = None
        best_profit = float("-inf")

        for plan_name, metrics in results.items():
            profit = metrics["total_profit"]
            if profit > best_profit:
                best_profit = profit
                best_name = plan_name

        return best_name if best_name is not None else "No data"