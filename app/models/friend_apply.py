from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from app.models import db
from flask_login import current_user


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

    def __repr__(self):
        return "<%s(id=%s,user=%s,friend=%s)>" % (
            self.__class__,
            self.id,
            self.user_id,
            self.friend_id,
        )

    @classmethod
    def find_send_from_me(cls):
        return cls.query.filter_by(user_id=current_user.id, apply_status=0).all()

    @classmethod
    def find_send_to_me(cls):
        return cls.query.filter_by(friend_id=current_user.id, apply_status=0).all()

    @classmethod
    def is_exist(cls, sender: int):
        return cls.query.filter_by(
            user_id=current_user.id, friend_id=sender, apply_status=0
        ).first()
