from . import db
from sqlalchemy.orm import Session

user_group_mapping = db.Table(
    "user_group_mapping",
    db.Column("user_id", db.Integer, db.ForeignKey("t_user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("t_group.id")),
    db.Column("role", db.SmallInteger, default=0)  # admin manager user
)


def do_find(user_id, group_id):
    session: Session = db.session
    query = user_group_mapping.select().where(
        (
                user_group_mapping.c.user_id == user_id
        ) & (
                user_group_mapping.c.group_id == group_id
        )
    )
    result = session.execute(query)
    return result.fetchall()
