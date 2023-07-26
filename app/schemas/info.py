from app.schemas import ma
from marshmallow import EXCLUDE, fields
from app.models.info import InformationModel
from app.schemas.base import BaseSchema


class InfoSelfSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta:
        model = InformationModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE
        partial = True
        exclude = ("user",)


class InfoOtherSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    class Meta:
        model = InformationModel
        load_instance = True
        unknown = EXCLUDE
        fields = ("id", "nickname", "avatar", "gender")
