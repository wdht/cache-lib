import os

CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
CACHE_BACKEND = os.environ.get('CACHE_BACKEND', 'null').lower()
CACHE_ENABLED = CACHE_BACKEND not in ['null', 'none', '']
CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
CACHE_KEY_PREFIX = os.environ.get('CACHE_KEY_PREFIX', '')


class Config:
    redis_url = CACHE_REDIS_URL
    backend = CACHE_BACKEND
    cache_enabled = CACHE_ENABLED
    cache_timeout = CACHE_DEFAULT_TIMEOUT
    cache_prefix = CACHE_KEY_PREFIX


config = Config()
