from . import db

from sqlalchemy import Column, Integer, String, ForeignKey

user_group_mapping = db.Table(
    "user_group_mapping",
    Column("user_id", Integer, ForeignKey("t_user.id")),
    Column("group_id", Integer, ForeignKey("t_group.id")),
    Column("join_time", Integer)  # admin manager user
)
# # member model

# class UserGroupMapping(db.Model):
#    user_id =  Column(Integer, ForeignKey("t_user.id"),primary_key=True)
#    group_id =  Column(Integer, ForeignKey("t_group.id"),primary_key=True)
#    join_time = Column(Integer)
