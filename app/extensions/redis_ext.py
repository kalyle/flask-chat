import redis


class RedisCache(object):
    def __init__(self) -> None:
        self.redis = None
        with app.app_context as app:
            self.host = app.config["REDIS_HOST"]
            self.port = app.config["REDIS_PORT"]

    def connect(self, db):
        self.redis = redis.Redis(host=self.host, port=self.port, db=db)


# string(短信，1)
# set(在线，3)
# hash(个人信息，单点登录，2)


redis = RedisCache()
