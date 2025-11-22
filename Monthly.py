import csv
import random
from typing import Dict, List, Optional, Sequence

from Dropout import Dropouts


class MonthlyChanges:
    def __init__(self, users: Dict[str, List], plan_names: Optional[Sequence[str]] = None):
        self.users = users
        self.plan_names = list(plan_names) if plan_names is not None else list(users.keys())
        self.month_names = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

    def migrate(self, source_group: str, dest_group: str, percent: float) -> None:
        """Move a percentage of people from one group to another."""
        src_list = self.users[source_group]
        amount = int(len(src_list) * percent)
        if amount == 0:
            return

        to_move = random.sample(src_list, amount)
        for user in to_move:
            src_list.remove(user)
            self.users[dest_group].append(user)

    @staticmethod
    def _display_user(user) -> str:
        if hasattr(user, "full_name"):
            return user.full_name
        if hasattr(user, "gamer_tag"):
            return user.gamer_tag
        return str(user)

    def apply_monthly_changes(self) -> None:
        """Simulate churn/migrations for one calendar year and write the CSV."""
        initial_users = []
        initial_counts = {}
        for group, user_list in self.users.items():
            initial_counts[group] = len(user_list)
            for user in user_list:
                initial_users.append((user, group))

        drop = Dropouts(self.users, plan_names=self.plan_names)

        with open("monthly_changes.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Month", *self.plan_names])

            for month in self.month_names:
                for group in self.plan_names:
                    percent = random.uniform(0.01, 0.05)
                    destination_candidates = [g for g in self.plan_names if g != group]
                    destination = random.choice(destination_candidates)
                    self.migrate(group, destination, percent)

                dropped = drop.apply_dropouts()

                writer.writerow([month, *[len(self.users[g]) for g in self.plan_names]])

                print(f"\n{month}:")
                for group in self.plan_names:
                    print(f"  {group:<9}: {len(self.users[group])}")
                drop.print_dropouts(dropped, month)

            writer.writerow([])
            writer.writerow(["Initial Number of Users per Plan"])
            for group in self.plan_names:
                writer.writerow([group, initial_counts[group]])

            writer.writerow([])
            writer.writerow(["Initial Users", "Plan"])
            for user, plan in initial_users:
                writer.writerow([self._display_user(user), plan])
