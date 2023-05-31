from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey,SmallInteger
from sqlalchemy.orm import relationship

class GroupApplyModel(BaseModel):
    __tablename__ = 't_group_apply'

    sender_id = Column(Integer, ForeignKey('t_user.id'))
    group_id = Column(Integer, ForeignKey('t_group.id'))
    note = Column(String(100), comment='留言')
    apply_status = Column(SmallInteger, default=0)  # 已添加，已删除，已拒绝