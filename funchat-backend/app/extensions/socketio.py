from flask_socketio import SocketIO

socketio = SocketIO()

from flask.views import MethodView


class View(MethodView):
    pass
