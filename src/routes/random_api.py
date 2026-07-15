from flask import Blueprint, jsonify, current_app, request
import random
import os

random_bp = Blueprint("random_api", __name__)

def get_seed():
    pool = current_app.config["POOL"]
    seed, updated = pool.get_seed()
    return seed, updated

@random_bp.route("/int")
def random_int():
    seed, updated = get_seed()
    if not seed:
        return jsonify({"success": False, "error": "seed_unavailable"}), 503

    low = request.args.get("min", 0, type=int)
    high = request.args.get("max", 0, type=int)

    rng = random.Random(f"{seed}{os.urandom(16).hex()}")    # os.urandom come salt
    value = rng.randint(low, high)

    return jsonify({"success": True, "value": value}), 200

@random_bp.route("/float")
def random_float():
    seed, updated = get_seed()
    if not seed:
        return jsonify({"success": False, "error": "seed_unavailable"}), 503

    low = request.args.get("min", 0, type=float)
    high = request.args.get("max", 0, type=float)

    rng = random.Random(f"{seed}{os.urandom(16).hex()}")    # os.urandom come salt
    value = rng.uniform(low, high)

    return jsonify({"success": True, "value": value}), 200

@random_bp.route("/choice")
def random_choice():
    seed, updated = get_seed()
    if not seed:
        return jsonify({"success": False, "error": "seed_unavailable"}), 503

    options = request.args.getlist("option")
    if not options:
        return jsonify({"success": False, "error": "missing_parameters"}), 400

    rng = random.Random(f"{seed}{os.urandom(16).hex()}")    # os.urandom come salt
    value = rng.choice(options)

    return jsonify({"success": True, "value": value}), 200