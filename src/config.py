import os

CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
CACHE_BACKEND = os.environ.get('CACHE_BACKEND', 'redis').lower()
CACHE_ENABLED = CACHE_BACKEND not in ['null', 'none', '']
CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
CACHE_KEY_PREFIX = os.environ.get('CACHE_KEY_PREFIX', '')
