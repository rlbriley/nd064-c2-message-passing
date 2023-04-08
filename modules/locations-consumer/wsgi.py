from __future__ import annotations
import logging
import json
import psycopg2

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
        cur = conn.cursor()
        cur.execute(f"SELECT MAX(id) FROM location;")
        rows = cur.fetchone()
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
            value = loc.value
            locationJson = json.loads(value)
            LocationService.create(locationJson)

    @staticmethod
    def create(location: Dict) :
        logger.info(f"Processing location: {location}")

        # Primary key so should only be one at max
        nextId = LocationService.get_next_id()
        cur = conn.cursor()
        # according to the documentation the latitude and longitude are backwards in
        # this statement. However it matches the code in the original query.
        query = f"INSERT INTO location (id, person_id, coordinate, creation_time) VALUES \
                 ({nextId}, {location['person_id']}, ST_GeomFromText(\'POINT({location['latitude']} {location['longitude']})\', 4326), \'{location['creation_time']}\');"
        logger.info(f"Query: {query}")
        cur.execute(query)
        conn.commit()

# Start the service. This method never returns!
LocationService.createThread()
