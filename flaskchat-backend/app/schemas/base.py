from . import ma
from marshmallow import fields, post_dump,pre_load


class BaseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.Time(dump_only=True)
    update_time = fields.Time(dump_only=True)
    status = fields.Integer(dump_only=True,default=0)

    @staticmethod
    def snake_to_camel(data: dict):
        # 下划线 转 驼峰
        pass

    @staticmethod
    def camel_to_sanke(data: dict):
        # 驼峰 转 下划线
        pass

    @pre_load
    def deserialize(self, data, **kwargs):
        return self.camel_to_sanke(data)

    @post_dump
    def serialize(self, data, **kwargs):
        return self.snake_to_camel(data)
