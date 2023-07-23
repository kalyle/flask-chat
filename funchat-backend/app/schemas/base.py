import re
from . import ma
from marshmallow import fields, post_dump, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.user import UserModel


class BaseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.Time(dump_only=True)
    update_time = fields.Time(dump_only=True)
    status = fields.Integer(dump_only=True, default=0)

    @staticmethod
    def snake_to_camel(data: dict):
        # 下划线 转 驼峰
        transed_data = {}
        for key, value in data.items():
            transed_data[re.sub(r"_([a-z])", lambda m: m.group(1).upper(), key)] = value
        return transed_data

    @staticmethod
    def camel_to_sanke(data: dict):
        # 驼峰 转 下划线
        transed_data = {}
        for key, value in data.items():
            transed_data[
                re.sub(r"([A-Z])", lambda m: f"_{m.group(1).lower()}", key)
            ] = value
        return transed_data

    @pre_load
    def deserializer(self, data, **kwargs):
        return self.camel_to_sanke(data)

    @post_dump
    def serializer(self, data, **kwargs):
        return self.snake_to_camel(data)
