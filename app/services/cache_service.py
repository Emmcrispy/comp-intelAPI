import redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6380))
REDIS_SSL = os.getenv("REDIS_SSL", "True").lower() == "true"
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=REDIS_SSL,
    decode_responses=True
)
r = redis.Redis(connection_pool=pool)

def cache_get(key: str):
    result = r.get(key)
    return json.loads(result) if result else None

def cache_set(key: str, data, ttl=3600):
    r.set(key, json.dumps(data), ex=ttl)
