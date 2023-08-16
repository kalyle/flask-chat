from flask_socketio import SocketIO
from flask_session import Session
from flask_cors import CORS
from flask_smorest import Api
from flask_migrate import Migrate
from flask_mail import Mail
import logging, os
from minio import Minio
import logging.config

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

# minio
minio_client = Minio(
    "1.12.236.91:9000",
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False,
)

# mail
mail = Mail()


# log
def init_logger():
    # 可改入cofig配置文件, 此处需对照logging.conf
    file_dir = r"./logs"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    logging.config.fileConfig("logging.conf")


# def get_logger(file_name):
#     file_path = f"./logs/{file_name}.log"
#     if not os.path.exists(file_path):
#         os.makedirs("./logs")
#     logger = logging.getLogger(file_name)
#     handler = logging.FileHandler(file_path, encoding='UTF-8')
#     logger.addHandler(handler)
#     return logger
