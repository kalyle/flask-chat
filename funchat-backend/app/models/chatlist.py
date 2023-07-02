from sqlalchemy import Column, SmallInteger, String, ForeignKey, Integer
from . import db


class ChatListModel(db.Model):
    __table_name__ = "chatList"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    avatar = Column(String(128))
    content = Column(String(255))
    chatTime = Column(String(128))
    type = Column(SmallInteger, default=0)
    user_id = Column(ForeignKey("t_user"))
