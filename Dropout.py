import random

class Dropouts:
    def __init__(self, users: dict):
     
        self.users = users

    def apply_dropouts(self):
        #plandan çıkma şansları için bir kod
        dropout_chance = 0.002
        monthly_dropped = []

        for group in ["Economic", "moderate", "luxurious"]:
            current_users = self.users[group][:]  # copy to avoid loop modification, verwirrend

            for user in current_users:
                if random.random() < dropout_chance:
                    monthly_dropped.append((user, group))
                    self.users[group].remove(user)

        return monthly_dropped

    def print_dropouts(self, dropped_users, month_name):
        """Kim çıkmışsa gösteriyor"""
        print(f"\nDropouts in {month_name}:")
        if not dropped_users:
            print("  No users dropped out.")
        else:
            for user, group in dropped_users:
                print(f"  {user} from {group} plan")
