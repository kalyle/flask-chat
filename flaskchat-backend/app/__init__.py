from flask import Flask
from flask_smorest import Api

from app.models import db
from app.schemas import ma
from app.api import api_v1

import settings


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.DevConfig)

    api = Api()
    with app.app_context():
        # db
        db.init_app(app)
        # api
        api.init_app(app)
        # ma
        ma.init_app(app)
        # cors
    
    api.register_blueprint(api_v1)
    return app