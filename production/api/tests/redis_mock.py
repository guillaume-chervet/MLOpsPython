from core.redis import Redis


class RedisMock(Redis):
    def __init__(self, logging):
        self.logger = logging.getLogger(__name__)

    def redis_hmset(self, key, data):
        self.logger.debug("redis_hmset :  " + key)

    def redis_hgetall(self, key):
        self.logger.debug("redis_hgetall :  " + key)
        return b"this is a mock"

    def redis_delete(self, key):
        self.logger.debug("redis_delete :  " + key)

    def redis_connection(self):
        return self.connection


class ConnectionMock:
    def jsonget(self, obj: str, path):
        return {}

    def jsonset(self, obj, path, value):
        return
