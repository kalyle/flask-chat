from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas.user import LoginSchema
from app.schemas.user import UserSelfSchema
from app.models.user import UserModel
from app.models import db
from flask_jwt_extended import create_access_token
from app.utils.reids import cache
import json

loginblp = Blueprint("login", "login", url_prefix="/login")


@loginblp.route("")
class Login(MethodView):
    @loginblp.arguments(
        LoginSchema(session=db.session), location="json", as_kwargs=True
    )
    @loginblp.response(200)
    def post(self, **login_data):
        user = UserModel.query.filter_by(username=login_data["username"]).first()
        if not user or not user.check_password(login_data["password"]):
            abort(400)
        user.token = create_access_token(identity=user)
        schema = UserSelfSchema()
        data = schema.dump(user)
        cache.hash_set("user_info", user.id, json.dumps(data))
        return data
