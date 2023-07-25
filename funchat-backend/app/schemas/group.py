from app.schemas import ma
from app.models.group import GroupModel


class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupModel
        load_instance = True
        exclude = ("user",)
