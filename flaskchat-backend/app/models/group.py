from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.user_group_mapping import UserGroupMapping


class GroupModel(BaseModel):
    __tablename__ = 't_group'

    name = Column(String(64), comment='群名')
    avatar = Column(String(255), comment='群头像')
    desc = Column(String(512), comment='简介')
    # setting = Column() 群的配置信息
    member_count = Column(Integer, comment='当前人数')
    owner_id = ForeignKey("t_user.id")
    adminer_id = ForeignKey("t_user.id")

    owner = relationship("UserModel", backref="groups_owned", lazy="dynamic")
    adminer = relationship("UserModel", backref="groups_admin", lazy="dynamic")
    messages = relationship("GroupChatRecordModel", backref="group", lazy="dynamic")
    group_apply_received = relationship('GroupApplyModel', backref='receiver',
                                        foreign_keys='GroupApplyModel.sender_id')
    members = relationship(
        'UserModel',
        secondary=UserGroupMapping,
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
        



