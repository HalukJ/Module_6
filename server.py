from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

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


@app.route("/<path:path>")
def static_proxy(path: str):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
