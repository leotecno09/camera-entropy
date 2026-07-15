from flask import Blueprint, jsonify, current_app, request
import random
import os
import base64
import string
import uuid as uuid_lib

tokens_bp = Blueprint("tokens_api", __name__)

def get_seed():
    pool = current_app.config["POOL"]
    seed, updated = pool.get_seed()
    return seed, updated

@tokens_bp.route("/uuid")
def random_uuid():
    seed, updated = get_seed()
    if not seed:
        return jsonify({"success": False, "error": "seed_unavailable"}), 503

    rng = random.Random(f"{seed}{os.urandom(16).hex()}")
    random_bits = rng.getrandbits(128)
    value = uuid_lib.UUID(int=random_bits, version=4)

    return jsonify({"success": True, "value": str(value)})

@tokens_bp.route("/string")
def random_string():
    seed, updated = get_seed()
    if not seed:
        return jsonify({"success": False, "error": "seed_unavailable"}), 503

    length = request.args.get("length", 16, type=int)
    charset_name = request.args.get("charset", "alphanumeric")

    if length > 256:
        return jsonify({"success": False, "error": "invalid_parameter: length (max is 256)"}), 400

    charsets = {
        "alphanumeric": string.ascii_letters + string.digits,
        "alpha": string.ascii_letters,
        "digits": string.digits,
        "hex": "0123456789abcdef",
    }

    charset = charsets.get(charset_name)
    if charset is None:
        return jsonify({"success": False, "error": f"invalid_parameter: charset (valid ones: {list(charsets)})"}), 400

    rng = random.Random(f"{seed}{os.urandom(16).hex()}")
    value = "".join(rng.choice(charset) for _ in range(length))

    return jsonify({"success": True, "value": value, "length": length, "charset": charset_name})
