import redis


class ChatCache(object):
    def __init__(self) -> None:
        self.redis = redis.StrictRedis(
            host="1.12.236.91", port=6379, decode_responses=True
        )

    # string
    def str_setex(self, key, val, expire):
        self.redis.setex(key, val, expire)

    def str_incr(self, key, expire=None):
        self.redis.incr(key)
        if expire is not None:
            self.redis.expire(key, expire)

    # set
    def set_add(self, key, *args):
        return self.redis.sadd(key, args)

    def set_rem(self, key, *args):
        return self.redis.srem(key, args)

    def set_ismember(self, key, val):
        return self.redis.sismember(key, val)

    def set_inter(self, key1, key2):
        # 交集
        return self.redis.sinter(key1, key2)

    def set_members(self, key):
        return self.redis.smembers(key)

    #


cache = ChatCache()
