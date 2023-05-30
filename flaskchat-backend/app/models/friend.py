from . import db
from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from sqlalchemy.orm import Session


class FriendModel(BaseModel):
    user_id = Column(Integer, ForeignKey('t_user.id'))
    friend_id = Column(Integer, ForeignKey('t_user.id'))
    remark = Column(String(126))
    top = Column(SmallInteger, default=0)
    apply_note = db.Column(db.String(100), comment='申请留言')
    apply_status = Column(SmallInteger, default=0)  # 已添加，已删除，已拉黑

    
    # foreign_keys接受类型 字符串、列表、字典
    user = db.relationship("UserModel", foreign_keys=[user_id],back_populate="friends")
    friend = db.relationship("UserModel", foreign_keys=[friend_id], back_populates="friends_with_me")

    @staticmethod
    def do_find(user_id, friend_id):
        session: Session = db.session
        query = FriendModel.select().where(
            (
                    FriendModel.c.get("user_id") == user_id
            ) & (
                    FriendModel.c.get("friend_id") == friend_id
            )
        )

        result = session.execute(query)
        return result.fetchall()

    @staticmethod
    def do_update(user_id, friend_id, update_data: dict):
        session: Session = db.session
        sql = FriendModel.select().where(
            (
                    FriendModel.c.get("user_id") == user_id
            ) & (
                    FriendModel.c.get("friend_id") == friend_id
            )
        ).values(**update_data)
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
            (
                    FriendModel.c.get("user_id") == user_id
            ) & (
                    FriendModel.c.get("friend_id") == friend_id
            )
        )
        session.execute(sql)
        session.commit()
