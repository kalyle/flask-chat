from . import db
from sqlalchemy.orm import Session

# user_group_mapping = db.Table(
#     "user_group_mapping",
#     db.Column("user_id", db.Integer, db.ForeignKey("t_user.id")),
#     db.Column("group_id", db.Integer, db.ForeignKey("t_group.id")),
#     db.Column("role", db.SmallInteger, default=0)  # admin manager user
# )
# member model

class UserGroupMapping(db.Model):
   user_id =  db.Column(db.Integer, db.ForeignKey("t_user.id"))
   group_id =  db.Column(db.Integer, db.ForeignKey("t_group.id"))
   join_time = db.Column(db.Date)
