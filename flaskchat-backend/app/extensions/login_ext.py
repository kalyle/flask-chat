from flask_login import LoginManager, UserMixin,current_user

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        return User(user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)