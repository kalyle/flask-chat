from flask import Flask

from app.models import db
from app.schemas import ma
from app.api import api_v1
from app import settings
from app.extensions.error_ext import handle_exception
from app.extensions.login_ext import login_manager
from app.extensions.init_ext import session, cors, api, migrate
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.DevConfig)
    app.config['SECRET_KEY'] = 'top-secret!'
    app.config['SESSION_TYPE'] = 'filesystem'
    print(os.getenv("MYSQL_HOST"))

    with app.app_context():
        # auth
        login_manager.init_app(app)
        # session
        session.init_app(app)
        # db
        db.init_app(app)
        # api
        api.init_app(app)
        # ma
        ma.init_app(app)
        # cors
        cors.init_app(app)
        # migrate
        migrate.init_app(app, db)

        # socketio.init_app(app)
        # return socketio ，Error: A valid Flask application was not obtained from 'flaskchat-backend.app:create_app()'
    api.register_blueprint(api_v1)
    # app.before_request(request_intercept)
    app.errorhandler(Exception)(handle_exception)
    return app
