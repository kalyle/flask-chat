from . import ma
from marshmallow import fields, post_load, pre_dump


class BaseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    create_by = fields.Str(dump_only=True)
    create_time = fields.Time(dump_only=True)
    status = fields.Integer(dump_only=True)

    # @pre_dump  # 序列化预处理
    # def serialize(self):
    #     pass
    #
    # @post_load  # 反序列化后处理
    # def deserialize(self):
    #     pass
