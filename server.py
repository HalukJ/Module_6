from __future__ import annotations

import os
import random
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, jsonify, request, send_from_directory

from database import GamePassDatabase, seed_database
from people import PeopleGenerator

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "frontend"
DB_PATH = BASE_DIR / "mudtpass.db"

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")

db = GamePassDatabase(DB_PATH)
db.initialize()
db.seed_if_empty(PeopleGenerator(1000, seed=42))

MONTH_NAMES = [
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


def _pick_new_plan(current: str, plan_order: List[str], rng: random.Random) -> str:
    """Lightweight migration helper that nudges users across tiers."""
    if len(plan_order) <= 1:
        return current
    candidates = [plan for plan in plan_order if plan != current]
    current_index = plan_order.index(current) if current in plan_order else 0
    weights = []
    for candidate in candidates:
        candidate_index = plan_order.index(candidate)
        # Favor mid-tier upgrades but de-emphasize the premium jump.
        if candidate_index > current_index and candidate_index < len(plan_order) - 1:
            weights.append(1.4)
        elif candidate_index > current_index:
            weights.append(0.9)
        else:
            weights.append(1.0)
    return rng.choices(candidates, weights=weights, k=1)[0]


def project_monthly_performance(db: GamePassDatabase, seed: int = 1337) -> Dict:
    """Simulate 12 months of playtime, migrations, and resulting profit."""
    catalog = db.get_plan_catalog()
    plan_order = catalog["order"]
    plan_prices = {name: catalog["plans"][name]["price"] for name in plan_order}
    plan_costs = {"Core": 0.12, "PC": 0.16, "Ultimate": 0.22}
    seasonal_variance = [1.02, 1.0, 0.96, 0.95, 0.97, 0.99, 1.05, 1.08, 1.04, 1.06, 1.1, 1.14]

    users = db.get_all_users()
    rng = random.Random(seed)
    user_states = [
        {
            "id": user["id"],
            "plan": user["plan"],
            "baseline_hours": user["hours_per_month"],
        }
        for user in users
    ]

    months = []
    for idx, month in enumerate(MONTH_NAMES):
        plan_totals = {plan: {"users": 0, "hours": 0} for plan in plan_order}

        for state in user_states:
            if rng.random() < 0.12:  # migrate a subset each month
                state["plan"] = _pick_new_plan(state["plan"], plan_order, rng)

            volatility = rng.uniform(0.85, 1.25)
            seasonal = seasonal_variance[idx % len(seasonal_variance)]
            hours = max(4, int(state["baseline_hours"] * volatility * seasonal))
            if state["plan"] == "Ultimate":
                hours = int(hours * 1.15)

            plan_totals[state["plan"]]["users"] += 1
            plan_totals[state["plan"]]["hours"] += hours

        month_payload = {"month": month, "plans": {}, "total_profit": 0.0, "total_hours": 0}
        for plan in plan_order:
            totals = plan_totals[plan]
            users_on_plan = totals["users"]
            total_hours = totals["hours"]
            revenue = users_on_plan * plan_prices[plan]
            cost_rate = plan_costs.get(plan, 0.15)
            cost = total_hours * cost_rate
            profit = round(max(revenue - cost, 0.0), 2)

            month_payload["plans"][plan] = {
                "users": users_on_plan,
                "avg_hours": round(total_hours / users_on_plan, 1) if users_on_plan else 0.0,
                "total_hours": total_hours,
                "profit": profit,
            }
            month_payload["total_profit"] += profit
            month_payload["total_hours"] += total_hours

        months.append(month_payload)

    return {"plan_order": plan_order, "months": months}


@app.route("/")
def index() -> str:
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/plans")
def plans():
    return jsonify(db.get_plan_catalog())


@app.post("/api/plans/favorite")
def favorite_plan():
    payload = request.get_json(silent=True) or {}
    plan = payload.get("plan")
    if not plan:
        return jsonify({"error": "Plan is required."}), 400
    try:
        catalog = db.set_favorite_plan(plan)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(catalog)


@app.route("/api/users/summary")
def user_summary():
    return jsonify(db.get_user_summary())


@app.route("/api/users/<plan>")
def users_by_plan(plan: str):
    limit = request.args.get("limit", default=8, type=int)
    plan = plan.title() if plan.islower() else plan
    users = db.get_users_by_plan(plan, limit=limit)
    return jsonify({"plan": plan, "users": users})


@app.post("/api/subscribe")
def subscribe():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    plan = payload.get("plan")
    if not name or not plan:
        return jsonify({"error": "Name and plan are required."}), 400
    try:
        user = db.subscribe_user(name, plan)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "status": "ok",
            "plan": user["plan"],
            "user": user,
            "summary": db.get_user_summary(),
        }
    )


@app.route("/api/analytics/monthly")
def monthly_projection():
    return jsonify(project_monthly_performance(db))


@app.route("/<path:path>")
def static_proxy(path: str):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
