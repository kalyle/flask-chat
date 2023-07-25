from .base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class FeedBackModel(BaseModel):
    __tablename__ = "feedback"

    title = Column(String(128), nullable=False, comment='回复标题')
    content = Column(String(255), nullable=False, comment='反馈内容')
    contact = Column(String(255), nullable=False, comment='反馈联系方式')
    user_id = Column(Integer, ForeignKey('user.id'), comment='创建人')
    feedback_type_id = Column(Integer, ForeignKey('feedback_type.id'), comment='反馈类型')
    feedback_type = relationship('FeedbackModel', backref="feedbacks")
    user = relationship('UserModel', backref="feedbacks")

    def __repr__(self):
        return "<%s(id=%s,title=%s,user=%s)>" % (
            self.__class__,
            self.id,
            self.title,
            self.user_id,
        )


class FeedbackTypeModel(BaseModel):
    __tablename__ = "feedback_type"
    name = Column(String(64), nullable=False, comment='反馈类型')


class FeedbackReplyModel(BaseModel):
    __tablename__ = 'feedback_reply'

    content = Column(String(255), nullable=False, comment='回复内容')
    feedback_id = Column(Integer, ForeignKey("feedback"))
    user_id = Column(Integer, ForeignKey('user.id'), comment='回复人')

    feedback = relationship('FeedbackModel', backref="feedback_replys")
    user = relationship('UserModel', backref="feedback_replys")
