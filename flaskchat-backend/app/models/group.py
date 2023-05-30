from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey,SmallInteger
from sqlalchemy.orm import relationship

from app.models.user_group_mapping import user_group_mapping


class GroupModel(BaseModel):
    __tablename__ = 't_group'

    name = Column(String(64), comment='群名')
    avatar = Column(String(255), comment='群头像')
    max_num = Column(Integer, comment='最大人数')
    desc = Column(String(512), comment='简介')
    creator_id = ForeignKey("t_user.id")

    messages = relationship("GroupChatRecordModel", backref="group", lazy="dynamic")
    group_apply_received = relationship('GroupApplyModel', backref='receiver',
                                        foreign_keys='GroupApplyModel.sender_id')
    members = relationship(
        'UserModel',
        secondary=user_group_mapping,
        back_populates="groups"
    )

    @classmethod
    def find_group_in_charge(cls):
        # 获取群申请的群主
        return cls.members.query.filter_by(role=0).first()


class GroupApplyModel(BaseModel):
    __tablename__ = 't_group_apply'

    sender_id = Column(Integer, ForeignKey('t_user.id'))
    group_id = Column(Integer, ForeignKey('t_group.id'))
    note = Column(String(100), comment='留言')
    status = Column(SmallInteger, default=0)  # 已添加，已删除，已拒绝