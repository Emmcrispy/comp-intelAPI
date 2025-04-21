# app/services/cache_service.py

"""
Local in-memory cache for development. Replaces Redis when not running in cloud.
"""

_cache = {}

def cache_get(key: str):
    return _cache.get(key)

def cache_set(key: str, data, ttl=3600):
    # TTL is ignored in this basic local implementation
    _cache[key] = data
