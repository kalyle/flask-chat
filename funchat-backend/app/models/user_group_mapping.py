from . import db
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, BigInteger, ForeignKey

user_group_mapping = db.Table(
    "user_group_mapping",
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("group_chat.id"), primary_key=True),
    Column("role", Integer, default=0),  # 0成员1管理员2群主
    Column("join_time", BigInteger),
    # Column("role", Integer)  # owner:2 admin:1 user:0
    # 群昵称，备注,发言权
)
