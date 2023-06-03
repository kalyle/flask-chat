from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class FriendChatRecordModel(BaseModel):
    """聊天记录"""
    __tablename__ = "t_friend_chat_record"

    sender_id = Column(Integer, ForeignKey("t_user.id"), comment="发送方")
    receiver_id = Column(Integer, ForeignKey("t_user.id"), comment="接受方")
    content = Column(String(500), nullable=False)

    sender = relationship("UserModel", foreign_keys=[sender_id],backref="friend_send_msg")
    receiver = relationship("UserModel", foreign_keys=[receiver_id], backref="friend_receive_msg")



class GroupChatRecordModel(BaseModel):
    __tablename__ = "t_group_chat_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("t_user.id"), comment="发送方")
    group_id = Column(Integer, ForeignKey("t_group.id"), comment="接受方")
    parent_id = Column(Integer,ForeignKey("t_group_chat_record.id"),comment="回复消息ID")
    content = Column(String(500), nullable=False)

    parent_id = Column(Integer, ForeignKey('t_group_chat_record.id'))
    parent = relationship('GroupChatRecordModel', remote_side=[id], backref='replys')
    sender = db.relationship("GroupModel", backref="group_send_msg")
    receiver = db.relationship("UserModel", backref="group_receive_msg")





# class ChatList(BaseModel):
#     """用于首页聊天列表记录"""
#     __tablename__ = "t_chat_list"
#
#     list_type = ((0, '机器人'), (1, '好友'), (2, '群聊'))
#
#     uid = Column(Integer, ForeignKey('t_user.id'))
#     lid = Column(Integer)
#     content = Column(String(500), nullable=False)
#     type = Column(ChoiceType(list_type, SmallInteger()), comment='类型')
#     list = relationship('User', backref='chat_list')
