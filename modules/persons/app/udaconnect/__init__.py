from app.udaconnect.models import Person  # noqa
from app.udaconnect.schemas import PersonSchema  # noqa


def register_routes(api, app, root="persons"):
    from app.udaconnect.controllers import api as udaconnect_persons

    api.add_namespace(udaconnect_api, path=f"/{root}")
