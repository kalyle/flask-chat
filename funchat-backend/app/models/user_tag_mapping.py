from sqlalchemy import Column, Integer, ForeignKey, BigInteger

from . import db
from .base import BaseModel
from app.models.tag import TagModel


class UserTagMappingModel(db.Model):
    __tablename__ = 'user_tag_mapping'

    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    liked_by_id = Column(Integer, ForeignKey('user.id'))
    create_time = Column(BigInteger)
    update_time = Column(BigInteger)
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
