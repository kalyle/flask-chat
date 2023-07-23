from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from app.models import db


class FriendApplyModel(BaseModel):
    __tablename__ = 'friend_apply'

    user_id = Column(Integer, ForeignKey('user.id'))
    friend_id = Column(Integer, ForeignKey('user.id'))
    type = Column(Integer, comment="好友来源")
    apply_note = Column(String(100), comment='验证信息')
    apply_status = Column(SmallInteger, default=0)  # 已添加，已删除，待验证(default)
    user = db.relationship(
        "UserModel", foreign_keys=[user_id], backref="to_friend_applys"
    )
    friend = db.relationship(
        "UserModel", foreign_keys=[friend_id], backref="from_friend_applys"
    )
