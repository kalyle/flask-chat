from . import db
from .base import BaseModel

from passlib.hash import pbkdf2_sha256
from app.models.friend import FriendModel
from app.models.group import GroupModel
from app.models.user_group_mapping import user_group_mapping


class UserModel(BaseModel):
    __tablename__ = 't_user'

    username = db.Column(db.String(64))
    password = db.Column(db.String(128), doc='密码')
    login_time = db.Column(db.DateTime, doc='登录时间')

    # info relationship
    info = db.relationship("InfoModel",uselist=False,backref="me")

    # friend relationship
    friends = db.relationship("FriendModel", foreign_keys=[FriendModel.user_id],back_populates="user")
    friends_with_me = db.relationship("FriendModel", foreign_keys=[FriendModel.friend_id], back_populates="friend")

    # group relationship
    groups_owned = db.relationship("GroupModel", foreign_keys=[GroupModel.owner_id],back_populates="owner")
    groups_admin = db.relationship("GroupModel", foreign_keys=[GroupModel.adminer_id],back_populates="adminers")
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
