from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from sqlalchemy.orm import Session


class FriendGroupModel(BaseModel):
    name = Column(String(100))
    # count = Column(Integer)
    user_id = Column(Integer, ForeignKey("t_user.id"))
