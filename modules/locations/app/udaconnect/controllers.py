import logging
import json

from app.udaconnect.models import Location
from app.udaconnect.schemas import (
    LocationSchema,
)
from app.udaconnect.services import LocationService
from flask import request, abort
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from kafka import KafkaProducer
from marshmallow import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-locations")

api = Namespace("UdaConnect", description="Connections via geolocation. Locations Microservice")  # noqa


TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-service.default.svc.cluster.local:9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

# TODO: This needs better exception handling

@api.route("/locations")
@api.route("/locations/<int:location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        locationJson = request.get_json()

        # send to kafka
        locStr = json.dumps(locationJson).encode('utf-8')
        logger.info(f"Adding Location to `locations` mailbox. '{locStr}'")

        producer.send(TOPIC_NAME, locStr)

        producer.flush()
        try:
            location = LocationSchema().load(locationJson)
        except ValidationError as err:
            logger.error(err.messages)

        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        if location_id is None:
            abort(400, description="location_id not provided")
        location: Location = LocationService.retrieve(location_id)
        if not location:
            abort(204, description="Resource not found")
        return location
