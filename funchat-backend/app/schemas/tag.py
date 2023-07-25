
from app.schemas import ma
from app.schemas.base import BaseSchema

from marshmallow import EXCLUDE

from app.models.tag import TagModel



class TagSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    class Meta:
        model = TagModel
        load_instance = True
        partial = True
        unknown = EXCLUDE
