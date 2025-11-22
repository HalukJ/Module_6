from Monthly import MonthlyChanges
from people import PeopleGenerator


def main():
    total_users = 1000  # <-- you can change this anytime

    print("\nGenerating Game Pass subscribers...")
    generator = PeopleGenerator(total_users)
    users = generator.generate()

    print("\nInitial distribution:")
    for plan in generator.plan_names:
        print(f"  {plan:<9}: {len(users[plan])}")

    print("\nPlan overview:")
    for plan in generator.plan_names:
        info = generator.plan_catalog[plan]
        perks = ", ".join(info["perks"])
        devices = "/".join(info["devices"])
        print(f"  {plan:<9} ${info['price']:.2f} - {info['description']} ({devices})")
        print(f"             Perks: {perks}")

    print("\nStarting monthly simulation...")
    monthly = MonthlyChanges(users, plan_names=generator.plan_names)
    monthly.apply_monthly_changes()

    print("\nSaved to: monthly_changes.csv")


if __name__ == "__main__":
    main()
