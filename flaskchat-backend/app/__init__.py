from flask import Flask
from .settings import config_map

from app.models import db
from app.schemas import ma
from app.api import api



def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config_map.get(config))

    with app.app_context():
        db.init_app(app)
        api.init_app(app)
        ma.init_app(app)

    return app