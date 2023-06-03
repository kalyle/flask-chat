from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from app.models import db
from app.schemas import ma
from app.api import api_v1

from app import settings


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.DevConfig)

    api = Api()
    migrate = Migrate()
    with app.app_context():
        # db
        db.init_app(app)
        # api
        api.init_app(app)
        # ma
        ma.init_app(app)
        # cors

        # migrate
        migrate.init_app(app,db)
    
    api.register_blueprint(api_v1)
    return app