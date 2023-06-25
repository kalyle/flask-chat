from flask_socketio import SocketIO

socketio = SocketIO(
    async_mode='eventlet',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    manage_session=True,
)
