from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from . import db

from app.models.user_group_mapping import user_group_mapping
from app.models.group_chat_record import GroupChatRecordModel
from app.models.group_apply import GroupApplyModel


class GroupChatModel(BaseModel):
    __tablename__ = 'group_chat'

    name = Column(String(64), comment='群名')
    avatar = Column(String(255), comment='群头像')
    description = Column(String(512), comment='简介')
    member_count = Column(Integer, comment='当前人数')
    setting_id = Column(Integer, ForeignKey('global_setting.id'))  # 群的配置信息
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = db.relationship(
        "UserModel", foreign_keys=[owner_id], back_populates="group_chats_owned"
    )
    members = db.relationship(
        'UserModel', secondary=user_group_mapping, back_populates="group_chats"
    )
    group_msg_received = db.relationship(
        "GroupChatRecordModel", back_populates="group_chat"
    )
    group_apply_received = db.relationship(
        'GroupApplyModel',
        primaryjoin='GroupChatModel.id==GroupApplyModel.group_id',
        back_populates="group_chat",
    )
    setting = db.relationship("GlobalSettingModel", backref="group_chat")

    @classmethod
    def find_group_in_charge(cls):
        # 获取群申请的群主
        return cls.members.query.filter_by(role=0).first()
