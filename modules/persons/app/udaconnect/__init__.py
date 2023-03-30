from app.udaconnect.models import Connection, Location, Person  # noqa
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa


def register_routes(persons, app, root="persons"):
    from app.udaconnect.controllers import api as udaconnect_persons

    api.add_namespace(udaconnect_persons, path=f"/{root}")
