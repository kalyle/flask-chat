from . import db
from .base import BaseModel

from passlib.hash import pbkdf2_sha256
from app.models.friend import FriendModel
from app.models.user_group_mapping import user_group_mapping


class UserModel(BaseModel):
    __tablename__ = 't_user'

    username = db.Column(db.String(64))
    password = db.Column(db.String(128), doc='密码')
    login_time = db.Column(db.DateTime, doc='登录时间')

    info = db.relationship("InfoModel",userlist=False,backref="me")

    # 定义与好友申请表的一对多关系
    friend_apply_sent = db.relationship('FriendApplyModel', backref='sender',foreign_keys='FriendApplyModel.sender_id')
    friend_apply_received = db.relationship('FriendApplyModel', backref='receiver',foreign_keys='FriendApplyModel.receiver_id')
    group_apply_sent = db.relationship('GroupApplyModel', backref='sender', foreign_keys='GroupApplyModel.sender_id')
    # 定义朋友关系
    friends = db.relationship("FriendModel", foreign_keys=[FriendModel.user_id],back_populates="user")
    friends_with_me = db.relationship("FriendModel", foreign_keys=[FriendModel.friend_id], back_populates="friend")

    create_group = db.relationship("GroupModel",backref="creator")
    groups = db.relationship(
        "GroupModel",
        secondary=user_group_mapping,
        back_populates="members"
    )

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
