from flask_jwt_extended import JWTManager

from app.models.user import UserModel

jwt = JWTManager()


# 用于向访问令牌中添加自定义声明，给token添加user_claims数据，在调用create_access_token函数时自动被调用
@jwt.additional_claims_loader
def add_claims_to_token(user):
    print("claims", user)
    return {
        "id": user.id,
    }


# 用于指定哪个属性应该作为访问令牌的标识，返回identity数据，在调用create_access_token函数时自动被调用
@jwt.user_identity_loader
def user_identity(user):
    print("user_identity", user)
    return user.id


# 回调函数，加载User实例
@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    print("jwt_data", jwt_data)
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none()


# current_user 必须要在@jwt_required()装饰器中使用,即必须经过验证后才能使用


@jwt.token_verification_failed_loader
def token_verification_fail(*args):
    print("验证失败", *args)
