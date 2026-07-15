from src.routes.random_api import random_bp
from src.routes.tokens_api import tokens_bp

def init_app(pool):
    from flask import Flask
    app = Flask(__name__)
    app.config["POOL"] = pool

    app.register_blueprint(random_bp, url_prefix="/api/random")
    app.register_blueprint(tokens_bp, url_prefix="/api/token")

    return app
