from flask_jwt_extended import current_user

from app.models import db
from sqlalchemy.orm import Session

from .base import BaseModel
from sqlalchemy import Column, String, Integer


class TagModel(BaseModel):
    __tablename__ = 'tag'

    name = Column(String(30))
    color = Column(String(30))
    created_by = Column(Integer)

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
            # logger
            session.rollback()
