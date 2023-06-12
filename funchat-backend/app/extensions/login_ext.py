from flask_login import LoginManager, UserMixin, login_user, logout_user
from app.models.user import UserModel

login_manager = LoginManager()


class User(UserMixin):
    def __init__(self, id: int):
        self.id = id

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        return User(user_id)

    @property
    def request_user(self) -> UserModel:
        return UserModel.find_by_id(self.id)

    # 单点登录
    def single_loign_user(self):
        # to do

        login_user(self)

    def single_logout_user(self):
        # to do

        logout_user(self)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
