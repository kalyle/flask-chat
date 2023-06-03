from flask.views import MethodView
from flask_smorest import Blueprint
from flask_login import login_required
from app.schemas.user import UserSelfSchema
from app.models.user import UserModel


accountblp = Blueprint("account","account",url_prefix="/account")

@accountblp.route("/register")
class Register(MethodView):
    @accountblp.arguments(UserSelfSchema,location="form")
    @accountblp.response(200,UserSelfSchema)
    def post(self,new_data):
        id = UserModel(**new_data).save_to_db()
        return UserModel.find_by_id(id)
    
@accountblp.route("/<user_id>/info")
class Info(MethodView):
    def get(self):
        # 获取指定user info
        return {}
    
    @login_required
    def patch(self):
        # 修改 user 信息
        return {}

@accountblp.route("/<user_id>/password/reset")
class PasswordReset(MethodView):
    @login_required
    def patch(self):
        return {}
    
@accountblp.route("/<user_id>/email/reset")
class EmailReset(MethodView):
    @login_required
    def patch(self):
        return {}

