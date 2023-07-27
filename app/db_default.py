from app.models.user import UserModel
from passlib.handlers.pbkdf2 import pbkdf2_sha256


def db_init():
    user = UserModel()
    user.id = -1
    user.username = "admin"
    user.password = pbkdf2_sha256.hash("123456")
    user.save_to_db()
