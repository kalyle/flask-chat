from app.extensions.socketio import socketio
from .chat import NotifyNamespace

socketio.on_namespace(NotifyNamespace('/notify'))
socketio.on_namespace(NotifyNamespace('/chat'))
