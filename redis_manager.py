# redis_manager.py
import redis

class RedisManager:
    def __init__(self, host='60.205.59.6', port=6326, password='uxin001'):
        self.redis_client = redis.Redis(host=host, port=port, db=0, password=password)
        self.redis_client1 = redis.Redis(host=host, port=6333, db=0, password=password)

    def delete_cache(self, key):
        """删除 Redis 缓存"""
        self.redis_client.delete(key)
        self.redis_client1.delete(key)

    def get_cache(self, key):
        """获取 Redis 缓存"""
        return self.redis_client.get(key), self.redis_client1.get(key)
