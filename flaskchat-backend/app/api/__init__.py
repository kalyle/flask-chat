from app.api.login import loginblp
from flask_smorest import Api
api = Api()
api.register_blueprint(loginblp)
api.register_blueprint(logoutblp)
api.register_blueprint(accountblp) 
api.register_blueprint(feedbackkblp)