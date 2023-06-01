from marshmallow import fields
from . import ma


class ResponseSchema(ma.Schema):
    code = fields.Integer(dump_only=True)
    msg = fields.String(dump_only=True)