from .base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class FeedBackModel(BaseModel):
    __tablename__ = "t_feedback"

    title = Column(String(128), nullable=False, comment='回复标题')
    image = Column(Text, comment='反馈问题截图')
    content = Column(Text, nullable=False, comment='反馈内容')
    contact = Column(String(128), comment='反馈联系方式')
    type_id = Column(Integer, ForeignKey('feedback_type.id'), comment='反馈类型')
    user_id = Column(Integer, ForeignKey('t_user.id'), comment='创建人')
    reply_id = Column(Integer, ForeignKey('feedback_reply.id'), comment='官方回复')


class FeedbackTypeModel(BaseModel):
    __tablename__ = "t_feedback_type"
    name = Column(String(64), unique=True, comment='反馈类型')
    feedbacks = relationship('Feedback', backref="feedbackType", lazy='dynamic')


class FeedbackReplyModel(BaseModel):
    __tablename__ = 't_feedback_reply'

    content = Column(Text, nullable=False, comment='回复内容')
    parent = Column(Integer, ForeignKey("t_feedback"))
    user_id = Column(Integer, ForeignKey('t_user.id'), comment='回复人')
