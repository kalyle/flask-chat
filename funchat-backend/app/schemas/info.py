from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE
from app.models.info import InformationModel


class InfoSelfSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InformationModel
        load_instance = True
        unknown = EXCLUDE
        exclude = ("user",)


class InfoOtherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InformationModel
        load_instance = True
        unknown = EXCLUDE
        fields = ("id", "nickname", "avatar", "gender")
