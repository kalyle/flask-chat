

from flask_principal import Principal, Permission,RoleNeed
from functools import wraps
principal = Principal()


# 定义相关角色
NORMAL = "NORMAL"
GROUP_OWNER = "GROUP_OWNER"
GROUP_ADMIN = "GROUP_ADMIN"
ADMIN = "ADMIN"
SUPER_ADMIN = "SUPER_ADMIN"

ROLES = (
    ("NORMAL","普通用户"),
    ("GROUP_ADMIN","群管理员"),
    ("GROUP_OWNER","群主"),
    ("ADMIN","管理员"),
    ("SUPER_ADMIN","超级管理员")
)

admin_permission = Permission(RoleNeed(ADMIN))

def admin_auth(func):
    @wraps(func)
    def decorated_view(*args,**kwargs):
        if admin_permission.can():
            return func(*args,**kwargs)
        else:
            return "非Admin用户"
    return decorated_view