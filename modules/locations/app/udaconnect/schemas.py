from app.udaconnect.models import Location
from geoalchemy2.types import Geometry as GeometryType
from marshmallow import Schema, fields
from marshmallow_sqlalchemy.convert import ModelConverter as BaseModelConverter


class LocationInit:
    def __init__(self, id, person_id, longitude, latitude, creation_time):
        self.id = id
        self.person_id = person_id
        self.longitude = longitude
        self.latitude = latitude
        self.creation_time = creation_time

    def __repr__(self)    :
        return f"{self.id}, {self.person_id}, {self.longitude}, {self.latitude}, {self.creation_time}"


class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.DateTime()

    class Meta:
        model = Location

    @post_load
    def create_location(felf, data, **kwargs):
        return LocationInit(**data)
