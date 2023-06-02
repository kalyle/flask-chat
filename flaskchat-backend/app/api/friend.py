from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify,request

from app.models.friend import FriendModel
from app.models.user import UserModel
from app.schemas.apply import ApplySendSchema,ApplyRecSchema
from flask_login import login_required,current_user

friendblp = Blueprint("friend", "friend", url_prefix="/friend")

@friendblp.route("")
class Friend(MethodView):
    @friendblp.response(200)
    @login_required
    def get(self):
        user = UserModel.find_by_id(current_user.id)
        friends = user.friends
        response = {}
        # 按照名字首字母排序分组
        return response
    
    @friendblp.response(200)
    def delete(self):
        friend_id = request.get_json()["friendId"]
        user_of_me = FriendModel.find_by_limit({"user_id":current_user.id,"friend_id":friend_id})
        friend_of_me = FriendModel.find_by_limit({"user_id":friend_id,"friend_id":current_user.id})

        user_of_me.delete_from_db()
        friend_of_me.delete_from_db()

        # emit status

        return {}


@friendblp.route("/apply")
class FriendApply(MethodView):
    @friendblp.response(200)
    # @login_required
    def get(self):
        # 自己发送的
        apply_from = FriendModel.find_by_limit({"user_id":current_user.id})
        apply_to = FriendModel.find_by_limit({"friend_id":current_user.id})

        response = {}
        response["fromApply"] = ApplySendSchema.dump(apply_from,many=True)
        response["toApply"] = ApplyRecSchema.dump(apply_to,many=True)

        return jsonify(response)

    @friendblp.arguments(ApplySendSchema,location="json")
    @friendblp.response(200,ApplySendSchema)
    # @login_user
    def post(self,new_data):
        # 重定向到好友聊天列表，并生成chatlist
        id = FriendModel(**new_data).save_to_db()
        # emit apply msg
        # emit(user,apply_response)
        return FriendModel.find_by_id(id)
    

@friendblp.route("/apply/<apply_id>")
class FriendApplyById(MethodView):
    @friendblp.response(200,ApplySchema)
    @login_required
    def get(self,apply_id):
        return FriendModel.find_by_id(apply_id)

    @friendblp.arguments(ApplyRecSchema,location="json",as_kwargs=True)
    @friendblp.response(200,ApplyRecSchema)
    # @login_required
    def patch(self,apply_id,**data):  # 这里路径参数 和 请求参数 顺序（如果是正常的，则路径参数在后？作为关键字参数，则在前？)
    
        apply_status = data["apply_status"]
        FriendModel.update_by_limit(apply_id,data)
        if apply_status == 1: # 同意
            # 成为好友
            FriendModel(user_id=data["friendId"],friend_id=data["userId"],apply_status=apply_status).save_to_db()
        response = FriendModel.find_by_id(apply_id)
        # emit apply msg
        # emit(user,apply_response)
            
        return response
    
    @friendblp.response(204)
    # @login_required
    def delete(self,apply_id):
        apply = FriendModel.find_by_id(apply_id)
        apply.delete_from_db()
        return {}
    

