from sqlalchemy.orm import Session

from app.models.base import BaseModel, db
from sqlalchemy import Column, String, Integer
from flask_login import current_user


class TagModel(BaseModel):
    __tablename__ = 'tag'

    name = Column(String(30), unique=True, nullable=False)
    color = Column(String(30), nullable=False)
    created_by = Column(Integer, default=-1, nullable=False)

    def __repr__(self):
        return "<%s(id=%s,name=%s,created_by=%s)>" % (
            self.__class__,
            self.id,
            self.name,
            self.created_by,
        )

    @classmethod
    def find_tags(cls):
        return cls.query.filter_by(created_by=-1).all()

    def save_to_db(self) -> int:
        session: Session = db.session
        self.created_by = current_user.id
        session.add(self)
        try:
            session.commit()
            return self.id
        except Exception as e:
            session.rollback()
