import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Person
from app.udaconnect.schemas import PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text, func

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-persons")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        # validation_results: Dict = LocationSchema().validate(person)
        # if validation_results:
        #     logger.warning(f"Unexpected data format in payload: {validation_results}")
        #     raise Exception(f"Invalid payload: {validation_results}")
        # Primary key so should only be one at max
        nextId = db.session.query(func.max(Person.id)).scalar()
        new_person = Person()
        new_person.id = nextId + 1
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).order_by(Person.id.asc()).all()
