from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models import db


class GroupModel(BaseModel):
    # 好友分组
    __tablename__ = "group"
    name = Column(String(20))
    count = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = db.relationship("UserModel", back_populates="groups")

    def __repr__(self) -> str:
        return "<%s(id=%s,name=%s,count=%s,user=%s)>" % (
            self.__class__,
            self.id,
            self.name,
            self.count,
            self.user_id,
        )
