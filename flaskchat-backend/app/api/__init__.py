from app.api.login import loginblp
from app.api.logout import logoutblp
from app.api.account import accountblp
from app.api.friend import friendblp
from flask_smorest import Blueprint


api_v1 = Blueprint("api/v1","api/v1", url_prefix="/api/v1")

api_v1.register_blueprint(loginblp)
api_v1.register_blueprint(logoutblp)
api_v1.register_blueprint(accountblp) 
api_v1.register_blueprint(friendblp)