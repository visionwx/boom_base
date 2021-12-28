import json
import redis
from .parameters import getRedisParaFromEnv

def create_redis_db(host='localhost', port=6379, 
    db=0, password=None, decode_responses=True):
    rdb = redis.StrictRedis(
        host=host, port=port, 
        db=db, password=password, 
        decode_responses=decode_responses)
    return rdb

class RedisBase():
    def __init__(self, redis_db):
        self.rdb = redis_db

    # 普通类型操作
    def keys(self, find):
        return self.rdb.keys(find)

    def exists(self, key):
        return self.rdb.exists(key)

    def set(self, key, value, ex=None):
        '''
            value：可接受string或者dict
            ex: 超时设置, 单位秒
        '''
        value = json.dumps(value)
        result = self.rdb.set(key, value, ex=ex)
        return result

    def get(self, key):
        value = self.rdb.get(key)
        if value is not None:
            value = json.loads(value)
        return value

    def delete(self, key):
        result = self.rdb.delete(key)
        return result

    def expire(self, key, ex=1):
        '''让某个key多久超时'''
        result = self.rdb.expire(key, ex)
        return result

    # hash类型操作
    def hset(self, hash_key, key, value):
        value = json.dumps(value)
        result = self.rdb.hset(hash_key, key, value)
        return result

    def hget(self, hash_key, key):
        value = self.rdb.hget(hash_key, key)
        value = json.loads(value)
        return value

    def hdel(self, hash_key, key):
        result = self.rdb.hdel(hash_key, key)
        return result

    # 数量统计
    def count(self, key_exp):
        return len(self.rdb.keys(key_exp))

# pubsub/subscribe的拓展
class RedisPubsubMixin():
    def init_pubsub(self):
        self.pubsub = self.rdb.pubsub(ignore_subscribe_messages=True)

    # 设置subscribe
    def set_subscribe(self, channel_name, func):
        if not channel_name in self.pubsub.channels:
            self.pubsub.subscribe(**{channel_name: func})

    # 检查和设置超时事件
    def check_and_set_notify_config(self):
        if self.rdb.config_get('notify-keyspace-events').get('notify-keyspace-events', '') == '':
            self.rdb.config_set('notify-keyspace-events', 'Ex')
        return True

class RedisDB(RedisBase, RedisPubsubMixin):
    def __init__(self, redisConfig):
        # redisConfig = getRedisParaFromEnv()
        redisDB = create_redis_db(**redisConfig)
        super().__init__(redisDB)

RDB = None
def getRedisDBInstance(
    host: str=None, 
    port: int=None, 
    db: int=None, 
    password: str=None, 
    decode_responses: str=None
):
    global RDB
    if RDB is not None:
        return RDB
    
    if host is None or port is None:
        raise Exception("redis host/port is None")
    redisConfig = {
        "host":  host,
        "port": port,
        "db": db,
        "password": password,
        "decode_responses": decode_responses,
    }
    RDB = RedisDB(redisConfig)
    return RDB

# if __name__ == "__main__":
#     rdb = getRedisDBInstance()
#     rdb.set("code", "123456")
#     code = rdb.get("code")
#     print(code)