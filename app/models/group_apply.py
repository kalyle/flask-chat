from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger

from . import db


class GroupApplyModel(BaseModel):
    __tablename__ = 'group_apply'

    sender_id = Column(Integer, ForeignKey('user.id'))
    group_id = Column(Integer, ForeignKey('group_chat.id'))
    type = Column(Integer, comment="好友来源")
    apply_note = Column(String(100), comment='留言')
    apply_status = Column(SmallInteger, default=0)  # 已添加，已删除，已拒绝

    group_chat = db.relationship(
        "GroupChatModel", back_populates="group_apply_received"
    )
    sender = db.relationship("UserModel", back_populates="group_apply_send")

    def __repr__(self):
        return "<%s(id=%s,sender=%s,group=%s)>" % (
            self.__class__,
            self.id,
            self.sender_id,
            self.group_id,
        )
