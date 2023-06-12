from . import db
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey

user_group_mapping = db.Table(
    "user_group_mapping",
    Column("user_id", Integer, ForeignKey("t_user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("t_group.id"), primary_key=True),
    Column("join_time", Integer)
    # Column("role", Integer)  # owner:2 admin:1 user:0
    # 群昵称，备注,发言权
)
