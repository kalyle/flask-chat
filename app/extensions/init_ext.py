from flask_socketio import SocketIO
from flask_session import Session
from flask_cors import CORS
from flask_smorest import Api
from flask_migrate import Migrate
import logging
from minio import Minio

# migrate
migrate = Migrate()

# socketio
socketio = SocketIO(
    async_mode='eventlet', cors_allowed_origins="*", manage_session=False
)

# session
session = Session()

# cors
cors = CORS(resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# api
api = Api()
# log
logger = logging.getLogger()
# minio
minio_client = Minio(
    "127.0.0.1:9000", access_key='minioadmin', secret_key='minioadmin', secure=False
)
