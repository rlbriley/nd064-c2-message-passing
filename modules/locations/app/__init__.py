import threading
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.udaconnect.services import LocationService
#from kafka.admin import KafkaAdminClient, NewTopic

db = SQLAlchemy()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-locations")


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API Locations", version="0.1.0")

    CORS(app)  # Set CORS for development

#    createKafkaTopics()

    logger.info("Creating thread for location service create.")
    x = threading.Thread(target=LocationService.createThread, daemon=True)
    x.start()

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("Locations Microservice healthy")

    return app

# def createKafkaTopics():
#     logger.info("Creating kafka topic 'locations'.")
#     admin_client = KafkaAdminClient(
#         bootstrap_servers="localhost:9092",
#         client_id='test'
#     )

#     topic_list = []
#     topic_list.append(NewTopic(name="locations", num_partitions=1, replication_factor=1))
#     admin_client.create_topics(new_topics=topic_list, validate_only=False)