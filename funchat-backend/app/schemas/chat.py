from flask_login import current_user
from marshmallow_sqlalchemy import SQLAlchemySchema
from app.schemas.base import BaseSchema
from marshmallow import fields, EXCLUDE, post_dump, pre_load


class FriendChatSchema(SQLAlchemySchema, BaseSchema):
    class Meta:
        load_instance = True


class GroupChatSchema(SQLAlchemySchema, BaseSchema):
    class Meta:
        load_instance = True
