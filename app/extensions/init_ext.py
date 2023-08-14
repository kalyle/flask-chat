from minio import Minio
from flask_socketio import SocketIO
import logging

# socketio
socketio = SocketIO(
    async_mode='eventlet', cors_allowed_origins="*", manage_session=False
)
# log
logger = logging.getLogger()
# minio
minio_client = Minio(
    "127.0.0.1:9000", access_key='minioadmin', secret_key='minioadmin', secure=False
)
