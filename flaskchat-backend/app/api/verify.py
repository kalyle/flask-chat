from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models.user import UserModel

verifyblp = Blueprint("verify", "verify", url_prefix="/verfiy")


@verifyblp.route("/mobile")
class VerifyMobile(MethodView):
    @verifyblp.response(200)
    def get(self):
        data = request.get_json()
        count = UserModel.find_by_limit(data)
        if count:
            abort(400, "电话已存在")
        return {}
