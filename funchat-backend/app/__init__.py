from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_socketio import SocketIO
from app.models import db
from app.schemas import ma
from app.api import api_v1
from flask_cors import CORS
from app import settings
from app.extensions.login_ext import login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.DevConfig)

    api = Api()
    migrate = Migrate()
    cors = CORS(resources={r"/*": {"origins": "*"}})

    with app.app_context():
        cors.init_app(app)
        # db
        db.init_app(app)
        # api
        api.init_app(app)
        # ma
        ma.init_app(app)
        # cors
        login_manager.init_app(app)
        # migrate
        migrate.init_app(app, db)

        # socketio.init_app(app)
        # return socketio ，Error: A valid Flask application was not obtained from 'flaskchat-backend.app:create_app()'

    api.register_blueprint(api_v1)
    return app
