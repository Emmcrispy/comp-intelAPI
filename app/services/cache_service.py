import redis
import json
from config.settings import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    ssl=True,
    decode_responses=True
)

r = redis.Redis(connection_pool=pool)

def cache_get(key: str):
    try:
        value = r.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        print(f"⚠️ Redis GET error: {e}")
        return None

def cache_set(key: str, data, ttl=3600):
    try:
        r.set(key, json.dumps(data), ex=ttl)
    except Exception as e:
        print(f"⚠️ Redis SET error: {e}")
