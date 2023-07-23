from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from . import db


class GroupChatRecordModel(BaseModel):
    __tablename__ = "group_chat_record"

    sender_id = Column(Integer, ForeignKey("user.id"), comment="发送方")
    group_chat_id = Column(Integer, ForeignKey("group_chat.id"), comment="接受方")
    content = Column(String(500), nullable=False)
    read = Column(Integer, default=0)
    is_reply = Column(Integer, default=False)
    reply_id = Column(Integer, ForeignKey("group_chat_record.id"), comment="回复消息")
    reply = db.relationship(
        'GroupChatRecordModel',
        remote_side="[GroupChatRecordModel.id]",
        backref='children',
    )  # remote_side用于自关联设置
    sender = db.relationship("UserModel", backref="group_msg_send")
    group_chat = db.relationship("GroupChatModel", back_populates="group_msg_received")
