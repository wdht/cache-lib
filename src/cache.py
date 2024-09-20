from typing import Optional
from . import config
from .cache_redis import BaseCache, RedisCache
from .models import Request, Response


def get_backend() -> BaseCache:
    if config.CACHE_BACKEND == 'redis':
        return RedisCache(
            config.CACHE_REDIS_URL,
            config.CACHE_DEFAULT_TIMEOUT,
            config.CACHE_KEY_PREFIX,
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
