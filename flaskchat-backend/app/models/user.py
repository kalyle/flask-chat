from sqlalchemy import Column,String,Integer

from . import db
from .base import BaseModel

from passlib.hash import pbkdf2_sha256
from app.models.friend import FriendModel
from app.models.group import GroupModel
from app.models.user_group_mapping import user_group_mapping


class UserModel(BaseModel):
    __tablename__ = 't_user'

    username = Column(db.String(64))
    password = Column(db.String(128), doc='密码')
    nickname = Column(String(64))
    avatar = Column(String(500), doc='用户头像图片')
    gender = Column(Integer, doc='用户性别')
    mobile = Column(String(11), doc='电话号码')
    email = Column(String(100), doc='邮箱')
    note = Column(String(500), doc='个性签名')
    login_time = Column(db.DateTime, doc='登录时间')
    is_active = Column(Integer)

    # friend relationship
    friends = db.relationship("FriendModel", foreign_keys=[FriendModel.user_id], back_populates="user")
    friends_with_me = db.relationship("FriendModel", foreign_keys=[FriendModel.friend_id], back_populates="friend")

    # group relationship
    groups_owned = db.relationship("GroupModel", foreign_keys=[GroupModel.owner_id], back_populates="owner")
    groups = db.relationship(
        "GroupModel",
        secondary=user_group_mapping,
        back_populates="members"
    )

    group_apply_send = db.relationship("GroupApplyModel",back_populates="sender")

    @property
    def password_salt(self):
        pass

    @password_salt.setter
    def password_salt(self, input_pwd):
        self.password = pbkdf2_sha256.hash(input_pwd)

    def check_password(self, input_pwd):
        return pbkdf2_sha256.verify(self.password, input_pwd)

    # @validates("email")
    # def validate_name(self, key, email):
    #     if re.match("", email):
    #         raise ValueError("Invalid email address")
    #     return email
