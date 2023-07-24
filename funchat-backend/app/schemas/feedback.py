from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.feedback import FeedBackModel, FeedbackTypeModel
from app.schemas.base import BaseSchema


class FeedBackSchema(SQLAlchemyAutoSchema, BaseSchema):
    class Meta:
        model = FeedBackModel
        load_instance = True
        partial = True


class FeedbackTypeSchema(SQLAlchemyAutoSchema, BaseSchema):
    class Meta:
        model = FeedbackTypeModel
        load_instance = True
        partial = True
