from sqlalchemy.orm import Query
from sqlalchemy import Column, Integer, ForeignKey, BigInteger, String

from . import db
from .base import BaseModel
from app.models.tag import TagModel


class UserTagMappingModel(BaseModel):
    __tablename__ = 'user_tag_mapping'

    tag_id = Column(Integer, ForeignKey('tag.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    liked_by_id = Column(Integer, ForeignKey('user.id'))
    images = Column(String(255))
    tag = db.relationship("TagModel", backref="user_tag_mapping")
    user = db.relationship("UserModel", foreign_keys=[user_id], backref="tags")
    liked_by = db.relationship(
        "UserModel", foreign_keys=[liked_by_id], backref="tag_liked_by"
    )

    def __repr__(self) -> str:
        return "<%s(tag=%s,user=%s,liked_by=%s)>" % (
            self.__class__,
            self.tag_id,
            self.user_id,
            self.liked_by_id,
        )

    @classmethod
    def find_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
