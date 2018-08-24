import aredis
from freeproxy.config import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


def getRedis():
    return aredis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)