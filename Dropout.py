import random
from typing import Dict, List, Optional, Sequence


class Dropouts:
    """Handle monthly customer churn for each subscription tier."""

    def __init__(
        self,
        users: Dict[str, List],
        plan_names: Optional[Sequence[str]] = None,
        min_percent: float = 0.01,
        max_percent: float = 0.03,
    ) -> None:
        # Keep a reference to the shared users dict so we can mutate it in-place.
        self.users = users
        self.plan_names = list(plan_names) if plan_names else list(users.keys())
        self.min_percent = min_percent
        self.max_percent = max_percent

    def _dropout_count(self, group: str) -> int:
        """
        Decide how many users should leave a given group this month.
        Ensures we never request more users than we have and that a positive
        dropout rate results in at least one departure when possible.
        """
        total = len(self.users[group])
        if total == 0:
            return 0

        percent = random.uniform(self.min_percent, self.max_percent)
        count = int(total * percent)
        if count == 0 and percent > 0:
            count = 1  # guarantee some churn if the group is non-empty
        return min(count, total)

    def apply_dropouts(self) -> Dict[str, List]:
        """
        Remove a small random portion of users from each group and return the
        list of removed users so it can be logged by the simulation.
        """
        dropped: Dict[str, List] = {}
        for group in self.plan_names:
            members = self.users[group]
            count = self._dropout_count(group)
            if count == 0:
                dropped[group] = []
                continue

            leaving = random.sample(members, count)
            for user in leaving:
                members.remove(user)
            dropped[group] = leaving

        return dropped

    def print_dropouts(self, dropped: Dict[str, List], month: str) -> None:
        """
        Print a short summary for the given month so the caller sees how many
        customers were lost per subscription plan.
        """
        total = sum(len(users) for users in dropped.values())
        if total == 0:
            print("  Dropouts : 0 (no churn this month)")
            return

        print(f"  Dropouts : {total}")
        for group in self.plan_names:
            count = len(dropped.get(group, []))
            print(f"    {group:<10} {count}")
