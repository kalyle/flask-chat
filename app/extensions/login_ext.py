from flask_login import LoginManager, UserMixin

login_manager = LoginManager()


class User(UserMixin):
    def __init__(self, id) -> None:
        self.id = id

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_load(user_id):
    return User(user_id)
