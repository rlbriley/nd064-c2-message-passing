import logging

from app.udaconnect.models import Location
from app.udaconnect.schemas import (
    LocationSchema,
)
from app.udaconnect.services import LocationService
from flask import request, abort
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from kafka import KafkaProducer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-locations")

api = Namespace("UdaConnect", description="Connections via geolocation. Locations Microservice")  # noqa


TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-service.default.svc.cluster.local:9092'

# TODO: This needs better exception handling

@api.route("/locations")
@api.route("/locations/<int:location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        locationJson = request.get_json()
        print(locationJson)
        logger.info(f"Adding Location to `locations` mailbox. {locationJson}")
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

        # send to kafka as a binary utf-8 object
        producer.send(TOPIC_NAME, locationJson.encode('utf-8'))
        producer.flush()
        return locationJson

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        if location_id is None:
            abort(400, description="location_id not provided")
        location: Location = LocationService.retrieve(location_id)
        if not location:
            abort(204, description="Resource not found")
        return location
