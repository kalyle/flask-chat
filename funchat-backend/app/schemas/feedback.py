from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.feedback import FeedBackModel, FeedbackTypeModel
from app.schemas.base import BaseSchema
from app.schemas import ma

class FeedBackSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    class Meta:
        model = FeedBackModel
        load_instance = True
        partial = True


class FeedbackTypeSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    class Meta:
        model = FeedbackTypeModel
        load_instance = True
        partial = True
