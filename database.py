import json
import random
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from people import GamePassUser, PeopleGenerator


class GamePassDatabase:
    """Simple SQLite wrapper to persist generated MUDTPass users and plans."""

    def __init__(self, path: str = "mudtpass.db") -> None:
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._random = random.Random()

    def initialize(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS plans (
                    name TEXT PRIMARY KEY,
                    display_order INTEGER NOT NULL,
                    price REAL NOT NULL,
                    tagline TEXT NOT NULL,
                    description TEXT NOT NULL,
                    best_for TEXT NOT NULL,
                    devices TEXT NOT NULL,
                    perks TEXT NOT NULL,
                    features TEXT NOT NULL,
                    hours_range TEXT NOT NULL,
                    is_favorite INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    gamer_tag TEXT NOT NULL,
                    plan TEXT NOT NULL,
                    preferred_device TEXT NOT NULL,
                    favorite_genre TEXT NOT NULL,
                    hours_per_month INTEGER NOT NULL,
                    backlog TEXT NOT NULL,
                    FOREIGN KEY(plan) REFERENCES plans(name)
                )
                """
            )
        self._ensure_favorite_column()
        self._ensure_default_favorite()

    def seed_if_empty(self, generator: PeopleGenerator) -> None:
        if self.count_users() > 0:
            return
        users = generator.generate()
        self.persist(generator.plan_catalog, generator.plan_names, users)

    def persist(
        self,
        plan_catalog: Dict[str, Dict],
        plan_order: Sequence[str],
        users: Dict[str, List[GamePassUser]],
    ) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM plans")
            self.conn.execute("DELETE FROM users")

            for order, plan in enumerate(plan_order):
                info = plan_catalog[plan]
                self.conn.execute(
                    """
                    INSERT INTO plans (
                        name, display_order, price, tagline, description, best_for,
                        devices, perks, features, hours_range, is_favorite
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        plan,
                        order,
                        info["price"],
                        info["tagline"],
                        info["description"],
                        info["best_for"],
                        json.dumps(info["devices"]),
                        json.dumps(info["perks"]),
                        json.dumps(info["features"]),
                        json.dumps(info["hours_range"]),
                        1 if order == 0 else 0,
                    ),
                )

            for plan, members in users.items():
                for member in members:
                    self.conn.execute(
                        """
                        INSERT INTO users (
                            full_name, gamer_tag, plan, preferred_device,
                            favorite_genre, hours_per_month, backlog
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            member.full_name,
                            member.gamer_tag,
                            member.plan,
                            member.preferred_device,
                            member.favorite_genre,
                            member.hours_per_month,
                            json.dumps(member.backlog),
                        ),
                    )

    def count_users(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) AS total FROM users").fetchone()
        return row["total"] if row else 0

    def get_plan_catalog(self) -> Dict:
        rows = self.conn.execute(
            "SELECT * FROM plans ORDER BY display_order ASC"
        ).fetchall()
        plan_data = {}
        order = []
        for row in rows:
            name = row["name"]
            order.append(name)
            plan_data[name] = {
                "name": name,
                "price": row["price"],
                "tagline": row["tagline"],
                "description": row["description"],
                "best_for": row["best_for"],
                "devices": json.loads(row["devices"]),
                "perks": json.loads(row["perks"]),
                "features": json.loads(row["features"]),
                "hours_range": tuple(json.loads(row["hours_range"])),
                "is_favorite": bool(row["is_favorite"]),
            }
        return {"order": order, "plans": plan_data}

    def get_user_summary(self) -> Dict:
        summary = {}
        rows = self.conn.execute(
            """
            SELECT plan, COUNT(*) AS count, AVG(hours_per_month) AS avg_hours
            FROM users
            GROUP BY plan
            """
        ).fetchall()
        for row in rows:
            summary[row["plan"]] = {
                "count": row["count"],
                "avg_hours": round(row["avg_hours"], 1) if row["avg_hours"] else 0,
                "top_genres": [],
                "top_devices": [],
            }

        for plan in summary.keys():
            genres = self.conn.execute(
                """
                SELECT favorite_genre, COUNT(*) AS c
                FROM users
                WHERE plan = ?
                GROUP BY favorite_genre
                ORDER BY c DESC
                LIMIT 2
                """,
                (plan,),
            ).fetchall()
            summary[plan]["top_genres"] = [row["favorite_genre"] for row in genres]

            devices = self.conn.execute(
                """
                SELECT preferred_device, COUNT(*) AS c
                FROM users
                WHERE plan = ?
                GROUP BY preferred_device
                ORDER BY c DESC
                LIMIT 2
                """,
                (plan,),
            ).fetchall()
            summary[plan]["top_devices"] = [row["preferred_device"] for row in devices]

        return summary

    def get_favorite_plan(self) -> Optional[str]:
        row = self.conn.execute(
            "SELECT name FROM plans WHERE is_favorite = 1 LIMIT 1"
        ).fetchone()
        return row["name"] if row else None

    def set_favorite_plan(self, plan: str) -> Dict:
        plan_row = self.conn.execute(
            "SELECT name FROM plans WHERE LOWER(name) = LOWER(?)",
            (plan,),
        ).fetchone()
        if not plan_row:
            raise ValueError("Unknown plan.")

        with self.conn:
            self.conn.execute("UPDATE plans SET is_favorite = 0")
            self.conn.execute(
                "UPDATE plans SET is_favorite = 1 WHERE LOWER(name) = LOWER(?)",
                (plan,),
            )

        return self.get_plan_catalog()

    def get_users_by_plan(self, plan: str, limit: int = 8) -> List[Dict]:
        rows = self.conn.execute(
            """
            SELECT full_name, gamer_tag, preferred_device, favorite_genre, hours_per_month
            FROM users
            WHERE plan = ?
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (plan, limit),
        ).fetchall()
        return [
            {
                "full_name": row["full_name"],
                "gamer_tag": row["gamer_tag"],
                "preferred_device": row["preferred_device"],
                "favorite_genre": row["favorite_genre"],
                "hours_per_month": row["hours_per_month"],
            }
            for row in rows
        ]

    def get_all_users(self) -> List[Dict]:
        """Return minimal user rows for analytics and simulations."""
        rows = self.conn.execute(
            "SELECT id, plan, hours_per_month FROM users"
        ).fetchall()
        return [
            {
                "id": row["id"],
                "plan": row["plan"],
                "hours_per_month": row["hours_per_month"],
            }
            for row in rows
        ]

    def subscribe_user(self, full_name: str, plan: str) -> Dict:
        if not full_name or not full_name.strip():
            raise ValueError("Name is required.")
        plan_row = self.conn.execute(
            "SELECT * FROM plans WHERE LOWER(name) = LOWER(?)",
            (plan,),
        ).fetchone()
        if not plan_row:
            raise ValueError("Unknown plan.")

        plan_name = plan_row["name"]
        devices = json.loads(plan_row["devices"])
        hours_low, hours_high = json.loads(plan_row["hours_range"])

        hours = self._random.randint(int(hours_low), int(hours_high))
        favorite_genre = self._random.choice(PeopleGenerator.GENRES)
        backlog_size = self._random.randint(1, min(4, len(PeopleGenerator.GAME_LIBRARY)))
        backlog = self._random.sample(PeopleGenerator.GAME_LIBRARY, k=backlog_size)
        preferred_device = self._random.choice(devices)
        gamer_tag = self._generate_gamer_tag()

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO users (
                    full_name, gamer_tag, plan, preferred_device,
                    favorite_genre, hours_per_month, backlog
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    full_name.strip(),
                    gamer_tag,
                    plan_name,
                    preferred_device,
                    favorite_genre,
                    hours,
                    json.dumps(backlog),
                ),
            )

        return {
            "full_name": full_name.strip(),
            "gamer_tag": gamer_tag,
            "plan": plan_name,
            "preferred_device": preferred_device,
            "favorite_genre": favorite_genre,
            "hours_per_month": hours,
            "backlog": backlog,
        }

    def _generate_gamer_tag(self) -> str:
        prefix = self._random.choice(PeopleGenerator.TAG_PREFIXES)
        suffix = self._random.choice(PeopleGenerator.TAG_SUFFIXES)
        digits = self._random.randint(10, 999)
        return f"{prefix}{suffix}{digits}"

    def _ensure_favorite_column(self) -> None:
        """Add the favorite flag to plans if an older DB is present."""
        cols = {
            row["name"]
            for row in self.conn.execute("PRAGMA table_info(plans)").fetchall()
        }
        if "is_favorite" in cols:
            return
        with self.conn:
            self.conn.execute(
                "ALTER TABLE plans ADD COLUMN is_favorite INTEGER NOT NULL DEFAULT 0"
            )

    def _ensure_default_favorite(self) -> None:
        """Make sure at least one plan is marked favorite for UX defaults."""
        favorite_count = self.conn.execute(
            "SELECT COUNT(*) AS total FROM plans WHERE is_favorite = 1"
        ).fetchone()
        if favorite_count and favorite_count["total"]:
            return
        top_plan = self.conn.execute(
            "SELECT name FROM plans ORDER BY display_order ASC LIMIT 1"
        ).fetchone()
        if not top_plan:
            return
        with self.conn:
            self.conn.execute("UPDATE plans SET is_favorite = 0")
            self.conn.execute(
                "UPDATE plans SET is_favorite = 1 WHERE name = ?", (top_plan["name"],)
            )


def seed_database(db_path: str = "mudtpass.db", total_users: int = 1000) -> None:
    generator = PeopleGenerator(total_users)
    db = GamePassDatabase(db_path)
    db.initialize()
    users = generator.generate()
    db.persist(generator.plan_catalog, generator.plan_names, users)


if __name__ == "__main__":  # pragma: no cover
    seed_database()
