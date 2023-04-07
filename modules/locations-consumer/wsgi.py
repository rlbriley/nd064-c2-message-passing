from __future__ import annotations
import logging
import os
import json
import psycopg2

from datetime import datetime
# from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
# from flask_cors import CORS
# from flask_restx import Api
# from werkzeug.exceptions import abort
# from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import text, func
from kafka import KafkaConsumer

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-service.default.svc.cluster.local:9092'
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locations-consumer")

conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
# db = SQLAlchemy()

# class Person(db.Model):
#     __tablename__ = "person"

#     id = Column(Integer, primary_key=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     company_name = Column(String, nullable=False)


# class Location(db.Model):
#     __tablename__ = "location"

#     id = Column(BigInteger, primary_key=True)
#     person_id = Column(Integer, ForeignKey(Person.id), nullable=False)
#     coordinate = Column(Geometry("POINT"), nullable=False)
#     creation_time = Column(DateTime, nullable=False, default=datetime.utcnow)
#     _wkt_shape = str(None)

#     @property
#     def wkt_shape(self) -> str:
#         # Persist binary form into readable text
#         if not self._wkt_shape:
#             point: Point = to_shape(self.coordinate)
#             # normalize WKT returned by to_wkt() from shapely and ST_AsText() from DB
#             self._wkt_shape = point.to_wkt().replace("POINT ", "ST_POINT")
#         return self._wkt_shape

#     @wkt_shape.setter
#     def wkt_shape(self, v: str) -> None:
#         self._wkt_shape = v

#     def set_wkt_with_coords(self, lat: str, long: str) -> str:
#         self._wkt_shape = f"ST_POINT({lat} {long})"
#         return self._wkt_shape

#     @hybrid_property
#     def longitude(self) -> str:
#         coord_text = self.wkt_shape
#         return coord_text[coord_text.find(" ") + 1 : coord_text.find(")")]

#     @hybrid_property
#     def latitude(self) -> str:
#         coord_text = self.wkt_shape
#         return coord_text[coord_text.find("(") + 1 : coord_text.find(" ")]

class LocationService:
    @staticmethod
    def get_next_id():
        logger.info(f"get_next_id()")
        # nextId: int = (db.session.query(func.max(Location.id)).scalar() + 1)
        # logger.info(f"query: {func.max(Location.id)}")
        cur = conn.cursor()
        cur.execute(func.max(Location.id))
        rows = cur.fetchall()
        nextId = row[0].scalar() + 1
        logger.info(f"get_next_id() exiting. nextId: {nextId}")
        return nextId

    @staticmethod
    def createThread():
        logger.info("Running location consumer thread.")
        locStr = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])

        for loc in locStr:
            # convert from utf-8 binary back to string
            logger.info(f"loc: {loc}")
            logger.info(f"loc type: {type(loc)}")
            value = loc.value
            logger.info(f"value: {value}")
            logger.info(f"value type: {type(value)}")
            locationJson = json.loads(value)
            logger.info(f"locationJson type: {type(locationJson)}")
            LocationService.create(locationJson)

    @staticmethod
    def create(location: Dict) -> Location:
        logger.info(f"Processing location: {location}")

        # Primary key so should only be one at max
        nextId = LocationService.get_next_id()
        # new_location = Location()
        # new_location.id = nextId
        # new_location.person_id = location["person_id"]
        # new_location.creation_time = location["creation_time"]
        # new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        # db.session.add(new_location)
        # db.session.commit()

        return new_location

# class BaseConfig:
#     CONFIG_NAME = "base"
#     USE_MOCK_EQUIVALENCY = False
#     DEBUG = True
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# class TestingConfig(BaseConfig):
#     CONFIG_NAME = "test"
#     SECRET_KEY = os.getenv("TEST_SECRET_KEY", "Thanos did nothing wrong")
#     DEBUG = True
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = (
#         f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     )

# def create_app(env=None):

#     logger.info("create_app()")
#     app = Flask(__name__)
#     app.config.from_object(TestingConfig)
#     api = Api(app, title="UdaConnect API Locations", version="0.1.0")

#     CORS(app)  # Set CORS for development

#     db.init_app(app)


#     @app.route("/health")
#     def health():
#         return jsonify("Locations Microservice healthy")

#     logger.info("create_app() complete")
#     return app

# app = create_app(os.getenv("FLASK_ENV") or "test")

# Start the service. This method never returns!
LocationService.createThread()


