from sqlalchemy import Column, String, BigInteger, ForeignKey

from . import db
from .base import BaseModel

from passlib.hash import pbkdf2_sha256
from app.models.friend import FriendModel
from app.models.group_chat import GroupChatModel
from app.models.user_group_mapping import user_group_mapping
from app.models.info import InformationModel
from app.models.user_tag_mapping import UserTagMappingModel
from app.models.group import GroupModel


class UserModel(BaseModel):
    __tablename__ = 'user'

    username = Column(String(64))
    password = Column(String(128), comment='密码')
    last_login_time = Column(BigInteger, comment='登录时间')
    # relationship
    information = db.relationship(
        "InformationModel", back_populates="user", uselist=False
    )
    # tags = db.relationship("UserTagMappingModel", primaryjoin='UserModel.id==UserTagMappingModel.tag_id',back_populates="user")
    # friend
    friends = db.relationship(
        "FriendModel", foreign_keys=[FriendModel.user_id], back_populates="user"
    )
    friends_with_me = db.relationship(
        "FriendModel", foreign_keys=[FriendModel.friend_id], back_populates="friend"
    )
    # group
    groups = db.relationship("GroupModel", back_populates="user")
    # group_chat
    group_chats_owned = db.relationship(
        "GroupChatModel", foreign_keys=[GroupChatModel.owner_id], back_populates="owner"
    )
    group_chats = db.relationship(
        "GroupChatModel", secondary=user_group_mapping, back_populates="members"
    )
    # group apply
    group_apply_send = db.relationship("GroupApplyModel", back_populates="sender")

    def __repr__(self):
        return "<%s(id=%s,username=%s)>" % (
            self.__class__,
            self.id,
            self.username,
        )

    @property
    def password_salt(self):
        pass

    @password_salt.setter
    def password_salt(self, input_pwd):
        self.password = pbkdf2_sha256.hash(input_pwd)

    def check_password(self, input_pwd):
        return pbkdf2_sha256.verify(input_pwd, self.password)

    # @validates("email")
    # def validate_name(self, key, email):
    #     if re.match("", email):
    #         raise ValueError("Invalid email address")
    #     return email
