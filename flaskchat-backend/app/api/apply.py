from flask.views import MethodView
from flask_smorest import Blueprint
from app.schemas.user import UserSchema
from app.models.user import UserModel
from app.models.friend import FriendModel
from flask_login import login_user

applyblp = Blueprint("apply", "apply", url_prefix="v1/apply")


@applyblp.route("/<user_id>")
class FriendApply(MethodView):
    @applyblp.response(200,ApplySchema(many=True))
    def get(self,user_id):
        # 自己发送的
        apply_list = FriendModel.query.filter_by(apply_status=3,sender_id=user_id,status=0).all()
        return apply_list
    
    def post(self):
        # 重定向到好友聊天列表，并生成chatlist
        return {}
    
    def delete(self):
        return {}
    
@applyblp.route("/<group_id>")
class GroupApply(MethodView):
    def get(self):
        return {}
    
    def post(self):
        
        return {}
    
    def delete(self):
        return {}
    