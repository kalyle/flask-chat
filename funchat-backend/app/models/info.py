from sqlalchemy import Column, String, Integer, ForeignKey

from . import db
from .base import BaseModel


class InformationModel(db.Model):
    __tablename__ = 'information'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    nickname = Column(String(64))
    avatar = Column(String(500), comment='用户头像图片')
    gender = Column(Integer, comment='用户性别')
    mobile = Column(String(11), comment='电话号码')
    email = Column(String(100), comment='邮箱')
    note = Column(String(500), comment='个性签名')
    birthday = Column(String(30))
    company = Column(String(30))
    address = Column(String(30))
    hometown = Column(String(30))

    user = db.relationship("UserModel", back_populates="information")

    def __repr__(self) -> str:
        return "<%s(id=%s)>" % (
            self.__class__,
            self.id,
        )
