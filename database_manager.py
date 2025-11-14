import sqlite3
import random
from typing import List, Dict


class DatabaseManager:
    """
    Handles SQLite connection and basic operations for NovaPlay Pass data.
    """

    def __init__(self, db_path: str = "nova_play_pass.db") -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create_tables(self) -> None:
        """
        Creates the users table if it does not exist.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    monthly_hours REAL NOT NULL,
                    current_plan TEXT NOT NULL
                );
                """
            )
            conn.commit()
        finally:
            conn.close()

    def seed_random_users(self, n_users: int = 40, clear_existing: bool = True) -> None:
        """
        Fills the database with random user data.
        Names are international, hours are random,
        and subscription choices may include 'none'.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            if clear_existing:
                cursor.execute("DELETE FROM users;")

            name_pool = [
                "Alice", "Bob", "Carlos", "Daria", "Eunji", "Farid", "Giulia",
                "Hiro", "Isabella", "Jonas", "Khalid", "Lena", "Mateo", "Nora",
                "Olivia", "Pablo", "Qi", "Rita", "Sven", "Tariq", "Uma",
                "Victor", "Wen", "Ximena", "Yara", "Zane", "Arjun", "Bianca",
                "Cem", "Deniz", "Elena", "Fiona", "Gustav", "Helena", "Ivan",
                "Julia", "Kaan", "Leyla"
            ]

            subscription_choices = ["Monthly", "Half-Year", "Yearly", "none"]

            for i in range(n_users):
                user_id = f"U{i+1:04d}"
                name = random.choice(name_pool)

                # Usage hours: simulate with a rough distribution (around 30-80 hours)
                # You can interpret this as an approximation of a Poisson-like distribution.
                monthly_hours = max(0.0, random.gauss(mu=50, sigma=15))

                current_plan = random.choice(subscription_choices)

                cursor.execute(
                    """
                    INSERT INTO users (user_id, name, monthly_hours, current_plan)
                    VALUES (?, ?, ?, ?);
                    """,
                    (user_id, name, monthly_hours, current_plan)
                )

            conn.commit()
        finally:
            conn.close()

    def fetch_all_users(self) -> List[Dict]:
        """
        Returns all users as a list of dictionaries.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, monthly_hours, current_plan FROM users;")
            rows = cursor.fetchall()
        finally:
            conn.close()

        users: List[Dict] = []
        for row in rows:
            users.append(
                {
                    "user_id": row[0],
                    "name": row[1],
                    "monthly_hours": float(row[2]),
                    "current_plan": row[3],
                }
            )
        return users