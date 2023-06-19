from flask_marshmallow import Marshmallow
from app.models import db

ma = Marshmallow()

# https://github.com/marshmallow-code/flask-marshmallow/issues/44
ma.SQLAlchemySchema.OPTIONS_CLASS.session = db.session
ma.SQLAlchemyAutoSchema.OPTIONS_CLASS.session = db.session
