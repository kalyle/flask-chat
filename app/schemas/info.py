from app.schemas import ma
from marshmallow import EXCLUDE
from app.models.info import InformationModel


class InfoSelfSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InformationModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE
        exclude = ("user",)


class InfoOtherSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InformationModel
        load_instance = True
        unknown = EXCLUDE
        fields = ("id", "nickname", "avatar", "gender")
