import redis

from config import settings


domain, host, port = settings.celery_broker_url.split(':')
host = host.split('//')[-1]
port = port.split('/')[0]


class RedisAPI:
    redis_connection = redis.Redis(host=host, port=port, decode_responses=True)
    def set_dict(self, name, obj):
        return self.redis_connection.hset(name, mapping=obj)
    
    def get_dict(self, name):
        return self.redis_connection.hgetall(name)

    def del_name(self, name):
        return self.redis_connection.hdel(name)
    
    def set_key(self, name, key_dict, value):
        return self.redis_connection.hset(name, key_dict, value)
    
    def get_key(self, name, key_dict):
        return self.redis_connection.hget(name, key_dict)

REDIS_API = RedisAPI()