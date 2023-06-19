from sqlalchemy import Column, Integer, String, ForeignKey
from . import db


class SettingModel(db.Model):
    __abstract__ = True
    top = Column(Integer)
    remark = Column(String(50))
    blacklist = Column(Integer)
    disturb = Column(Integer, comment="免打扰")
    hide = Column(Integer)
    background = Column(String(255))
    online_notice = Column(Integer, default=0)

    friend_id = Column(Integer, ForeignKey("t_friend.id"), primary_key=True)
