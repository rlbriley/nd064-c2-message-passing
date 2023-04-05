import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text, func
from kafka import KafkaConsumer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-locations")

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    # def nextId():
    #     nextId = db.session.query(func.max(Location.id)).scalar()
    #     return nextId

    # @staticmethod
    # def create(location: Dict) -> Location:
    #     logger.info("Processing location: " + json.dumps(location, 4) )

    #     # Primary key so should only be one at max
    #     nextId = db.session.query(func.max(Location.id)).scalar()
    #     new_location = Location()
    #     new_location.id = nextId + 1
    #     new_location.person_id = location["person_id"]
    #     new_location.creation_time = location["creation_time"]
    #     new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
    #     db.session.add(new_location)
    #     db.session.commit()

    #     return new_location
