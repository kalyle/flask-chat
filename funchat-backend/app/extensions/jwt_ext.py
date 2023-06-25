from flask_jwt_extended import JWTManager

from app.models.user import UserModel

jwt = JWTManager()


# 用于向访问令牌中添加自定义声明
@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    return {
        "id": user.id,
    }


# 用于指定哪个属性应该作为访问令牌的标识
@jwt.user_identity_loader
def user_identity(user):
    return user.id


# 回调函数，加载User实例
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    print("jwt_data", jwt_data)
    identity = jwt_data["id"]
    return UserModel.query.filter_by(id=identity).one_or_none()
