from people import PeopleGenerator
from Monthly import MonthlyChanges

def main():
   
    total_users = 1000  # <-- you can change this anytime
    
    # -------- GENERATE PEOPLE --------
    print("\nGenerating users...")
    generator = PeopleGenerator(total_users)
    users = generator.generate()

    print("Initial distribution:")
    print("  Economic :", len(users["Economic"]))
    print("  Moderate :", len(users["moderate"]))
    print("  Luxurious:", len(users["luxurious"]))

    # -------- APPLY MONTHLY CHANGES --------
    print("\nStarting monthly simulation...")
    monthly = MonthlyChanges(users)
    monthly.apply_monthly_changes()

    print()
    print("Saved to:  monthly_changes.csv")

if __name__ == "__main__":
    main()
