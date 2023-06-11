from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from . import db

from app.models.user_group_mapping import user_group_mapping
from app.models.chat import GroupChatRecordModel, FriendChatRecordModel
from app.models.apply import GroupApplyModel


class GroupModel(BaseModel):
    __tablename__ = 't_group'

    name = Column(String(64), comment='群名')
    avatar = Column(String(255), comment='群头像')
    desc = Column(String(512), comment='简介')
    # setting = Column() 群的配置信息
    member_count = Column(Integer, comment='当前人数')
    owner_id = Column(Integer, ForeignKey('t_user.id'))

    owner = db.relationship("UserModel", foreign_keys=[owner_id], back_populates="groups_owned")
    group_msg_received = db.relationship("GroupChatRecordModel", back_populates="group")
    group_apply_received = db.relationship('GroupApplyModel',
                                           primaryjoin='GroupModel.id==GroupApplyModel.group_id',
                                           back_populates="group"
                                           )
    members = db.relationship(
        'UserModel',
        secondary=user_group_mapping,
        back_populates="groups"
    )

    @classmethod
    def find_group_in_charge(cls):
        # 获取群申请的群主
        return cls.members.query.filter_by(role=0).first()

    @staticmethod
    def is_over(group_id):
        obj = GroupModel.query.filter_by(id=group_id).first()
        return obj.member_count == obj.setting.member_count
