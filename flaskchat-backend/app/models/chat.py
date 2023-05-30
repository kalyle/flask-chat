from . import db
from .base import BaseModel


class FriendChatRecordModel(BaseModel):
    """聊天记录"""
    __tablename__ = "t_friend_chat_record"

    sender_id = db.Column(db.Integer, db.ForeignKey("t_user.id"), comment="发送方")
    receiver_id = db.Column(db.Integer, db.ForeignKey("t_user.id"), comment="接受方")
    content = db.Column(db.String(500), nullable=False)


class GroupChatRecordModel(BaseModel):
    __tablename__ = "t_group_chat_record"

    sender_id = db.Column(db.Integer, db.ForeignKey("t_user.id"), comment="发送方")
    group_id = db.Column(db.Integer, db.ForeignKey("t_group.id"), comment="接受方")
    content = db.Column(db.String(500), nullable=False)

# class ChatList(BaseModel):
#     """用于首页聊天列表记录"""
#     __tablename__ = "t_chat_list"
#
#     list_type = ((0, '机器人'), (1, '好友'), (2, '群聊'))
#
#     uid = db.Column(db.Integer, db.ForeignKey('t_user.id'))
#     lid = db.Column(db.Integer)
#     content = db.Column(db.String(500), nullable=False)
#     type = db.Column(ChoiceType(list_type, SmallInteger()), comment='类型')
#     list = db.relationship('User', backref='chat_list')
