from flask_socketio import SocketIO, Namespace

socketio = SocketIO()


class SocketView(Namespace):
    # 对ws请求添加login_requires装饰器
    decorators = {}

    def __new__(cls):
        return super().__new__(cls)
