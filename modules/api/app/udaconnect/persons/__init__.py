from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from models import Person  # noqa
from schemas import PersonSchema  # noqa


db = SQLAlchemy()


def register_routes(api, root="api"):
    from controllers import api as udaconnect_api

    add_namespace(udaconnect_api, path=f"/{root}")

def create_app(env=None):
    from config import config_by_name
    from routes import register_routes

    app = Flask(__name__)
    config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API Persons", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
