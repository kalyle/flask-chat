from flask import Flask
from .settings import config_map

from app.models import db
from app.schemas import ma
from app.api import api

from app.extension.permission import principal

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config_map.get(config))

    
    with app.app_context():
        # db
        db.init_app(app)
        # api
        api.init_app(app)
        # ma
        ma.init_app(app)
        # cors

        # principal
        principal.init_app(app)
    
    return app