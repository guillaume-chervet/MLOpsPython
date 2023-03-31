from json import JSONEncoder
from rejson import Client, Path
import os


class AppSettingsRedis:
    def __init__(self):
        self.host_redis = os.getenv("redis_host", "redis-ha-haproxy")
        self.port_redis = int(os.getenv("redis_port", "6379"))
        self.expire_time = int(os.getenv("redis_expire_time", "60"))
        self.expire_time_debug = int(os.getenv("redis_expire_time_debug", "120"))


def get_is_debug():
    return False


class Redis:
    def __init__(self, app_setting=AppSettingsRedis(), local_get_is_debug=get_is_debug):
        self.expire_time = app_setting.expire_time
        self.expire_time_debug = app_setting.expire_time_debug
        self.connection = Client(host=app_setting.host_redis, port=app_setting.port_redis, retry_on_timeout=True)
        self.jsonconnection = Client(
            host=app_setting.host_redis, port=app_setting.port_redis, encoder=JSONEncoder(ensure_ascii=False),
            retry_on_timeout=True, decode_responses=True
        )
        self.local_get_is_debug = local_get_is_debug

    def redis_hmset(self, key, data):
        self.connection.hmset(key, data)

        expire_time = self.expire_time
        if self.local_get_is_debug():
            expire_time = self.expire_time_debug
        self.connection.expire(key, expire_time)

    def redis_hgetall(self, key):
        return self.connection.hgetall(key)

    def redis_connection(self):
        return self.jsonconnection, Path

    def redis_delete(self, key):
        self.connection.delete(key)
