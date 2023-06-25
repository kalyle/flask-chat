import os, datetime


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "DEV_KEY") or 'secret!'
    API_TITLE = "FlaskChat"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    CORS_SUPPORTS_CREDENTIALS = True

    JWT_SECRET_KEY = ""
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    # 连接池
    # SQLALCHEMY_POOL_SIZE = 0
    # SQLALCHEMY_POOL_TIMEOUT = 0
    # SQLALCHEMY_POOL_RECYCLE = 0
    # SQLALCHEMY_MAX_OVERFLOW = 0


class DevConfig(Config):
    EVN = "dev"
    DEBUG = True

    # sqlalchemy
    MYSQL_HOST = os.getenv("MYSQL_HOST") or "127.0.0.1"
    MYSQL_PORT = int(os.getenv("MYSQL_PORT") or "3306")
    MYSQL_USERNAME = os.getenv("MYSQL_USERNAME") or "root"
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD") or "root"
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE") or "flaskchat"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # smorest
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
