from sqlalchemy import Column, SmallInteger, String, ForeignKey, Integer, BigInteger
from . import db


class ChatListModel(db.Model):
    __tablename__ = "chat_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    avatar = Column(String(128))
    content = Column(String(255))
    type = Column(SmallInteger, default=0)
    create_time = Column(BigInteger)
    user_id = Column(ForeignKey("user"))
    user = db.relationship("UserModel", backref="chat_lists")
