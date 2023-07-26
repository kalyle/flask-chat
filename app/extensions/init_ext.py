from minio import Minio
from flask_socketio import SocketIO

socketio = SocketIO(
    async_mode='eventlet',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    manage_session=True,
)
minio_client = Minio(
    "127.0.0.1:9000", access_key='minioadmin', secret_key='minioadmin', secure=False
)
