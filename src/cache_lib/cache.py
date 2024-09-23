from typing import Optional
from .config import config
from .cache_redis import BaseCache, RedisCache
from .models import Response


def get_backend() -> BaseCache:
    if config.backend == 'redis':
        return RedisCache(
            config.redis_url,
            config.cache_timeout,
            config.cache_prefix,
        )


class Cache:
    def __init__(self):
        self.backend = get_backend()

    def get_request(self, key: str) -> Optional[Response]:
        if self.backend is None:
            return None
        return self.backend.get(key)

    def store_response(self, key: str, response: Response, timeout=None):
        if self.backend is None:
            return None
        kwargs = {'key': key, 'value': response}
        if timeout is not None:
            kwargs['timeout'] = timeout
        self.backend.set(**kwargs)
