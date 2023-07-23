from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models import db


class FriendChatRecordModel(BaseModel):
    __tablename__ = "friend_chat_record"

    sender_id = Column(Integer, ForeignKey("user.id"), comment="发送方")
    receiver_id = Column(Integer, ForeignKey("user.id"), comment="接受方")
    content = Column(String(500), nullable=False)
    read = Column(Integer, default=0, nullable=False)
    is_reply = Column(Integer, default=0, nullable=False)
    reply_id = Column(Integer, ForeignKey("friend_chat_record.id"), comment="回复消息")

    sender = db.relationship(
        "UserModel", foreign_keys=[sender_id], backref="send_from_me"
    )  # db.relationship和sqlalchemy.orm.relationship不同
    receiver = db.relationship(
        "UserModel", foreign_keys=[receiver_id], backref="send_to_me"
    )
    reply = db.relationship(
        'FriendChatRecordModel',
        remote_side="[FriendChatRecordModel.id]",
        backref='children',
    )  # remote_side用于自关联设置
