import random
import csv
from Dropout import Dropouts

class MonthlyChanges:
    def __init__(self, users: dict):

        self.users = users
        self.month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

    def migrate(self, source_group, dest_group, percent):
        """Move a percentage of people from one group to another."""
        src_list = self.users[source_group]
        amount = int(len(src_list) * percent)
        if amount == 0:
            return  # nothing to move

        # Rastgele birini seç
        to_move = random.sample(src_list, amount)

        # yerlerini değiştir
        for user in to_move:
            src_list.remove(user)
            self.users[dest_group].append(user)

    def apply_monthly_changes(self):
       

        # İlk hallerini CSV'ye kaydediyoruz
        initial_users = []
        for group, user_list in self.users.items():
            for user in user_list:
                initial_users.append((user, group))

        drop = Dropouts(self.users)

        with open("monthly_changes.csv", "w", newline="") as file:
            writer = csv.writer(file)
            # Header for monthly summary
            writer.writerow(["Month", "Economic", "Moderate", "Luxurious"])

            for month in self.month_names:
                # Each group loses 1–5% to OTHER groups
                for group in ["Economic", "moderate", "luxurious"]:
                    percent = random.uniform(0.01, 0.05)
                    destination = random.choice(
                        [g for g in ["Economic", "moderate", "luxurious"] if g != group]
                    )
                    self.migrate(group, destination, percent)

                # Apply dropouts
                dropped = drop.apply_dropouts()

                # Write monthly summary to CSV
                writer.writerow([
                    month,
                    len(self.users["Economic"]),
                    len(self.users["moderate"]),
                    len(self.users["luxurious"])
                ])

                # Print short summary to terminal
                print(f"\n{month}:")
                print("  Economic :", len(self.users['Economic']))
                print("  Moderate :", len(self.users['moderate']))
                print("  Luxurious:", len(self.users['luxurious']))

                # Print dropouts
                drop.print_dropouts(dropped, month)
                 # kullanıcı sayısı
                writer.writerow([]) 
                writer.writerow(["Initial Number of Users per Plan"])
                for group, user_list in self.users.items():
                    writer.writerow([group, len(user_list)])


            # plana göre kişiler belki hesapları tekrar eklediğimizde ordakileri değiştirebileceğimizden tutuyorum
            writer.writerow([]) 
            writer.writerow(["Initial Users", "Plan"])
            for user, plan in initial_users:
                writer.writerow([user, plan])
            writer.writerow([" MM  MM"])
            writer.writerow(["M   M   M"])
            writer.writerow([" M    M"])
            writer.writerow(["   MM"])


         
