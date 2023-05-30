from . import db
from sqlalchemy.orm import Session, Query


class BaseModel(db.Model):
    __abstract__ = True
    query: Query

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # create_by = db.Column(db.String)
    create_time = db.Column(db.Date)
    update_time = db.Column(db.Date)

    @classmethod
    def find_by_id(cls):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> int:
        session: Session = db.session
        session.add(self)
        try:
            session.commit()
            return self.id
        except Exception as e:
            # logger
            session.rollback()

    def delete_from_db(self) -> None:
        session: Session = db.session
        session.delete(self)
        try:
            session.commit()
        except:
            session.rollback()
