from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.group import GroupModel


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GroupModel
        load_instance = True
        exclude = ("user",)
