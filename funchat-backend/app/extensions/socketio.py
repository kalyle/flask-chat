from flask_socketio import SocketIO, Namespace, emit

socketio = SocketIO(
    async_mode='eventlet',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
)


class SocketView(Namespace):
    # 对ws请求添加login_requires装饰器
    decorators = {}

    def __new__(cls, name, parents, attrs):
        decorators_attrs = {}
        for key, val in attrs.items():
            if key.startswith("on_"):
                pass
            else:
                decorators_attrs[key] = name
        return type.__new__(cls, name, parents, attrs)


@socketio.on("sendMsg")
def sendmsg(msg):
    print('msg', msg)
    emit('my_response', {'data': "connected"})


@socketio.on('message')
def receive(msg):
    print(msg)
    return True
