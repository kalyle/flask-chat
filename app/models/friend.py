from . import db
from app.models.base import BaseModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Session
from app.models.global_setting import GlobalSettingModel


class FriendModel(BaseModel):
    __tablename__ = 'friend'

    user_id = Column(Integer, ForeignKey('user.id'))
    friend_id = Column(Integer, ForeignKey('user.id'))
    setting_id = Column(Integer, ForeignKey('global_setting.id'))
    favorite = Column(Integer, default=0, comment="特别关心")
    block = Column(Integer, default=0, comment="拉黑")
    type = Column(Integer, comment="好友来源")
    # foreign_keys接受类型 字符串、列表、字典
    user = db.relationship(
        "UserModel", foreign_keys=[user_id], back_populates="friends"
    )
    friend = db.relationship(
        "UserModel", foreign_keys=[friend_id], back_populates="friends_with_me"
    )
    setting = db.relationship("GlobalSettingModel", backref="friend")

    def __repr__(self):
        return "<%s(id=%s,user=%s,friend=%s)>" % (
            self.__class__,
            self.id,
            self.user_id,
            self.friend_id,
        )

    # 适用于中间表
    # @staticmethod
    # def do_find(user_id, friend_id):
    #     session: Session = db.session
    #     query = FriendModel.select().where(
    #         (FriendModel.c.get("user_id") == user_id)
    #         & (FriendModel.c.get("friend_id") == friend_id)
    #     )

    #     result = session.execute(query)
    #     return result.fetchall()

    # @staticmethod
    # def do_update(user_id, friend_id, update_data: dict):
    #     session: Session = db.session
    #     sql = (
    #         FriendModel.select()
    #         .where(
    #             (FriendModel.c.get("user_id") == user_id)
    #             & (FriendModel.c.get("friend_id") == friend_id)
    #         )
    #         .values(**update_data)
    #     )
    #     session.execute(sql)
    #     session.commit()

    # @staticmethod
    # def do_insert(insert_data: dict):
    #     session: Session = db.session

    #     sql = FriendModel.insert().values(**insert_data)
    #     session.execute(sql)
    #     session.commit()

    # @staticmethod
    # def do_delete(user_id, friend_id):
    #     session: Session = db.session
    #     sql = FriendModel.delete().where(
    #         (FriendModel.c.get("user_id") == user_id)
    #         & (FriendModel.c.get("friend_id") == friend_id)
    #     )
    #     session.execute(sql)
    #     session.commit()
