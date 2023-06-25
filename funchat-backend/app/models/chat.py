from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from . import db


class FriendChatRecordModel(BaseModel):
    """聊天记录"""

    __tablename__ = "t_friend_chat_record"

    sender_id = Column(Integer, ForeignKey("t_user.id"), comment="发送方")
    receiver_id = Column(Integer, ForeignKey("t_user.id"), comment="接受方")
    content = Column(String(500), nullable=False)
    # read = Column(Boolean, default=False)

    sender = relationship(
        "UserModel", foreign_keys=[sender_id], backref="friend_send_msg"
    )
    receiver = relationship(
        "UserModel", foreign_keys=[receiver_id], backref="friend_receive_msg"
    )


class GroupChatRecordModel(BaseModel):
    __tablename__ = "t_group_chat_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("t_user.id"), comment="发送方")
    group_id = Column(Integer, ForeignKey("t_group.id"), comment="接受方")
    parent_id = Column(Integer, ForeignKey("t_group_chat_record.id"), comment="回复消息ID")
    content = Column(String(500), nullable=False)
    # read = Column(Boolean, default=False)

    parent = relationship(
        'GroupChatRecordModel', remote_side=[id], backref='replys'
    )  # remote_side用于自关联设置
    sender = db.relationship("UserModel", backref="group_msg_send")
    group = db.relationship("GroupModel", back_populates="group_msg_received")
