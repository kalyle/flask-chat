from app.schemas import ma
from app.schemas.base import BaseSchema

from marshmallow import EXCLUDE
from app.schemas.tag import TagSchema
from app.models.user_tag_mapping import UserTagMappingModel
from app.schemas.user import UserOtherSchema


class UserTagMappingSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    tag = ma.Nested(TagSchema(exclude=("created_by")))
    liked_by = ma.Nested(UserOtherSchema(many=True))

    class Meta:
        model = UserTagMappingModel
        load_instance = True
        partial = True
        unknown = EXCLUDE
        exclude = ("user",)
