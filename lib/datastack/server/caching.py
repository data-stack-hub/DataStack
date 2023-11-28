from cachetools import TTLCache


cache_storage = {}


class Cache_data:
    def __init__(self, func_has):
        cache_storage[func_has] = self

        self.mem_cache: TTLCache[str, bytes] = TTLCache(maxsize=10, ttl=180)

    def mem_cache_set(self, key, value):
        self.mem_cache[key] = value

    def mem_cache_get(self, key):
        return self.mem_cache[key]
