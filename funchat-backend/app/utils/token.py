class Token:
    """
    生成token，用于单点登录，和 apifox登录权限接口测试
    生成类似于current_app的token
    """

    token = ""

    def __init__(self):
        pass

    def generate(self):
        return self.token

    def refresh(self):
        return self.token


# request_stack
