from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Nested

from app.models.friend import FriendModel

from app.schemas.base import BaseSchema
from app.schemas.user import UserOtherSchema


class ApplyScheam(SQLAlchemySchema,BaseSchema):
    friend = Nested(UserOtherSchema)
    class Meta:
        model = FriendModel
        include_pk = True
        fields = ["user_id","friend","apply_note","apply_status"]