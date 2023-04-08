from __future__ import annotations
import logging
import os
import json
import psycopg2

from datetime import datetime
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_Point
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

class LocationService:
    @staticmethod
    def get_next_id():
        logger.info(f"get_next_id()")
        # nextId: int = (db.session.query(func.max(Location.id)).scalar() + 1)
        # logger.info(f"query: {func.max(Location.id)}")
        cur = conn.cursor()
        cur.execute(f"SELECT MAX(id) FROM location;")
        rows = cur.fetchone()
        logger.info(f"rows: {rows}")
        # Should be a single row with a single value.
        nextId = rows[0] + 1
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
    def create(location: Dict) :
        logger.info(f"Processing location: {location}")

        # Primary key so should only be one at max
        nextId = LocationService.get_next_id()
        cur = conn.cursor()
        query = f"INSERT INTO location SET(id, person_id, coordinate, creation_time) VALUES \
                 ({nextId}, {location['person_id']}, \'{ST_Point(location['latitude'], location['longitude'])}\', \'{location['creation_time']}\');"
        logger.info(f"Query: {query}")
        cur.execute(query)
        conn.commit();

        return new_location

# Start the service. This method never returns!
LocationService.createThread()


