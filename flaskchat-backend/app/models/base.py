from . import db
from sqlalchemy.orm import Session, Query
from flask_sqlalchemy.model import Model

class BaseModel(db.Model):
    __abstract__ = True
    query: Query

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.Date)
    update_time = db.Column(db.Date)

    @classmethod
    def find_by_id(cls):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_limit(cls,find_data):
        data = cls.get_limits(cls,find_data)
        return cls.query.filter_by(data).all()
    
    @classmethod
    def update_by_limit(cls,id,update_data:dict):
        session:Session = db.session
        data = cls.get_limits(cls,update_data)
        
        try:
            cls.query.filter_by(id=id).update(data)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False

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

    @staticmethod
    def get_limits(cls,data):
        model_columns = set(column.name for column in cls.__table__.columns)
        return {k:v for k,v in data.items() if k in model_columns}