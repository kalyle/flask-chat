from . import db
from .base import BaseModel

class InfoModel(db.Model):
    nickname = db.Column(db.String(64))
    avatar = db.Column(db.String(500), doc='用户头像图片')
    gender = db.Column(db.Integer, doc='用户性别')
    email = db.Column(db.String(100), doc='邮箱')
    note = db.Column(db.String(500), doc='备注')
    mobile = db.Column(db.String(11), doc='电话号码')

    user_id = db.Column(db.Foreignkey("t_user.id"))
    