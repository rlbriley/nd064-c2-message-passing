
from models import Person
from schemas import (
    PersonSchema,
)
from services import PersonService
from flask import Flask, abort
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

api = Namespace("UdaConnectPersons", description="Connections via geolocation. Person microservice")  # noqa


# TODO: This needs better exception handling

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons

@api.route("/persons/<int:person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        if person_id is None:
            abort(400, description="person_id not provided")
        person: Person = PersonService.retrieve(person_id)
        if not person:
            abort(204, description="Resource not found")
        return person
