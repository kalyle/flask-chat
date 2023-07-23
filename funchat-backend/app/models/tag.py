from flask_jwt_extended import current_user

from .base import BaseModel
from sqlalchemy import Column, String, Integer, or_


class TagModel(BaseModel):
    __tablename__ = 'tag'

    name = Column(String(30))
    created_by = Column(Integer)

    def __repr__(self):
        return "<%s(name=%s,created_by=%s)>" % (
            self.__class__,
            self.name,
            self.created_by,
        )

    @classmethod
    def find_tags(cls):
        return cls.query.filter(
            or_(cls.created_by == -1, cls.created_by == current_user.id)
        ).all()
