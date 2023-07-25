from flask_marshmallow import Marshmallow
from app.models import db

ma = Marshmallow()

# https://github.com/marshmallow-code/flask-marshmallow/issues/44
ma.SQLAlchemySchema.OPTIONS_CLASS.session = db.session
ma.SQLAlchemyAutoSchema.OPTIONS_CLASS.session = db.session

from app.schemas.register import RegisterSchema
from app.schemas.info import InfoOtherSchema, InfoSelfSchema
from app.schemas.user import UserSelfSchema
