from . import db
from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from sqlalchemy.orm import Session


class FriendModel(BaseModel):
    __tablename__ = 't_friend'

    user_id = Column(Integer, ForeignKey('t_user.id'))
    friend_id = Column(Integer, ForeignKey('t_user.id'))

    apply_note = Column(String(100), comment='申请留言')
    apply_status = Column(SmallInteger, default=0)  # 已添加，已删除
    # setting
    # setting = db.relationship("SettingModel",backref="friend")

    # foreign_keys接受类型 字符串、列表、字典
    user = db.relationship(
        "UserModel", foreign_keys=[user_id], back_populates="friends"
    )
    friend = db.relationship(
        "UserModel", foreign_keys=[friend_id], back_populates="friends_with_me"
    )

    # 适用于中间表
    @staticmethod
    def do_find(user_id, friend_id):
        session: Session = db.session
        query = FriendModel.select().where(
            (FriendModel.c.get("user_id") == user_id)
            & (FriendModel.c.get("friend_id") == friend_id)
        )

        result = session.execute(query)
        return result.fetchall()

    @staticmethod
    def do_update(user_id, friend_id, update_data: dict):
        session: Session = db.session
        sql = (
            FriendModel.select()
            .where(
                (FriendModel.c.get("user_id") == user_id)
                & (FriendModel.c.get("friend_id") == friend_id)
            )
            .values(**update_data)
        )
        session.execute(sql)
        session.commit()

    @staticmethod
    def do_insert(insert_data: dict):
        session: Session = db.session

        sql = FriendModel.insert().values(**insert_data)
        session.execute(sql)
        session.commit()

    @staticmethod
    def do_delete(user_id, friend_id):
        session: Session = db.session
        sql = FriendModel.delete().where(
            (FriendModel.c.get("user_id") == user_id)
            & (FriendModel.c.get("friend_id") == friend_id)
        )
        session.execute(sql)
        session.commit()


class FriendGroupByModel(db.Model):
    __tablename__ = 'friend_groupby'

    name = Column(String(100))
    user_id = Column(ForeignKey("t_user.id"), primary_key=True)
    user = db.relationship("UserModel", back_populates="groupby")
