from sqlalchemy import Column, Integer, String

from app.models import db


class GlobalSettingModel(db.Model):
    __tablename__ = 'global_setting'
    id = Column(Integer, primary_key=True, autoincrement=True)
    top = Column(Integer, comment="置顶")
    remark = Column(String(50), comment="备注")
    mute = Column(Integer, default=0, comment="免打扰")
    hide = Column(Integer, comment="隐藏会话")
    background = Column(String(255), comment="聊天背景")

    def __repr__(self):
        return "<%s(id=%s)>" % (self.__class__, self.id)
