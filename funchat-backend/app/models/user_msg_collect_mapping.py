from sqlalchemy import Column, ForeignKey

from . import db

user_msg_collect_mapping = db.Table(
    "user_msg_collect_mapping",
    Column("user_id", ForeignKey("t_user.id"), primary_key=True),
    Column("msg_id", ForeignKey("t_friend_record.id"), primary_key=True),
)
