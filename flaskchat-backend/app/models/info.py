from . import db

from sqlalchemy import Column, Integer, String, ForeignKey


class InfoModel(db.Model):
    user_id = Column(Integer, ForeignKey('t_user.id'),primary_key=True)
    nickname = Column(String(64))
    avatar = Column(String(500), doc='用户头像图片')
    gender = Column(Integer, doc='用户性别')
    mobile = Column(String(11), doc='电话号码')
    email = Column(String(100), doc='邮箱')
    note = Column(String(500), doc='备注')
    

    
