from marshmallow_sqlalchemy import SQLAlchemySchema

from app.schemas.base import BaseSchema
from app.schemas.user import UserOtherSchema
from marshmallow import fields


class ApplySchema(SQLAlchemySchema,BaseSchema):
    user_id = fields.Integer(dump_only=True)
    friend_id = fields.Integer(dump_only=True)
    apply_note = fields.String()
    apply_status = fields.Integer()

class ApplySendSchema(ApplySchema,BaseSchema):
    friend = fields.Nested(UserOtherSchema)
    
class ApplyRecSchema(ApplySchema,BaseSchema):
    user = fields.Nested(UserOtherSchema)
    