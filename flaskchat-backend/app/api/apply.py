from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify
from app.schemas.apply import ApplySendSchema,ApplyRecSchema
from app.models.friend import FriendModel
from flask_login import login_user,current_user
applyblp = Blueprint("apply", "apply", url_prefix="v1/apply")


@applyblp.route("/friend")
class FriendApply(MethodView):
    @applyblp.response(200)
    # @login_user
    def get(self):
        # 自己发送的
        apply_from = FriendModel.find_by_limit({"user_id":current_user.id})
        apply_to = FriendModel.find_by_limit({"friend_id":current_user.id})

        response = {}
        response["fromApply"] = ApplySendSchema.dump(apply_from,many=True)
        response["toApply"] = ApplyRecSchema.dump(apply_to,many=True)

        return jsonify(response)

    @applyblp.arguments(ApplySendSchema,location="json")
    @applyblp.response(200)
    # @login_user
    def post(self,new_data):
        # 重定向到好友聊天列表，并生成chatlist
        id = FriendModel(**new_data).save_to_db()
        # 通知 friend 好友申请，发送一个信号给socketio
        return FriendModel.find_by_id(id)
    

@applyblp.route("/<apply_id>/friend")
class GroupApply(MethodView):
    @applyblp.arguments(ApplyRecSchema,location="json",as_kwargs=True)
    @applyblp.response(200,ApplyRecSchema)
    # @login_user
    def patch(self,apply_id,**data):  # 这里路径参数 和 请求参数 顺序（如果是正常的，则路径参数在后？作为关键字参数，则在前？)
        data["user_id"] = current_user.id
        apply_id = int(apply_id)
        FriendModel.update_by_limit(apply_id,data)
        return FriendModel.find_by_id(apply_id)
    
    @applyblp.response(204)
    # @login_user
    def delete(self,apply_id):
        apply = FriendApply.find_by_id(int(apply_id))
        apply.update_by_limit({"status":1})
        return {}
    