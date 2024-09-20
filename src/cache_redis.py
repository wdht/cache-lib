import pickle
from typing import Optional
from .cache_base import BaseCache


class RedisCache(BaseCache):
    """Uses the Redis key-value store as a cache backend.

    The first argument can be either a string denoting address of the Redis
    server or an object resembling an instance of a redis.Redis class.

    Note: Python Redis API already takes care of encoding unicode strings on
    the fly.
    Any additional keyword arguments will be passed to ``redis.Redis``.
    """
    object_marker = b'.'

    def __init__(
        self,
        connection_string: str,
        default_timeout: int = 300,
        key_prefix: Optional[str] = None,
        **kwargs
    ):
        super().__init__(default_timeout)
        try:
            import redis
        except ImportError:
            raise RuntimeError('Could not import redis')
        client = redis.Redis.from_url(connection_string, **kwargs)

        self.client = client
        self.key_prefix = key_prefix or ''

    def _normalize_timeout(self, timeout):
        timeout = super()._normalize_timeout(timeout)
        if timeout == 0:
            timeout = -1
        return timeout

    def dump_object(self, value):
        """
        Dumps an object into a string for redis. Integers are serialized
        as regular strings, arbitrary objects are dumped with pickle.
        """
        if isinstance(value, int):
            return str(value).encode('ascii')
        return self.object_marker + pickle.dumps(value)

    def load_object(self, value):
        """
        The reversal of :meth:`dump_object`.  This might be called with None.
        """
        if value is None:
            return None
        if value.startswith(self.object_marker):
            try:
                return pickle.loads(value[1:])
            except pickle.PickleError:
                return None
        return int(value)

    def get(self, key):
        return self.load_object(self.client.get(self.key_prefix + key))

    def get_many(self, *keys):
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]
        return [self.load_object(x) for x in self.client.mget(keys)]

    def set(self, key, value, timeout=None):
        timeout = self._normalize_timeout(timeout)
        dump = self.dump_object(value)
        if timeout == -1:
            result = self.client.set(
                name=self.key_prefix + key, value=dump
            )
        else:
            result = self.client.setex(
                name=self.key_prefix + key, value=dump, time=timeout
            )
        return result

    def set_many(self, mapping, timeout=None):
        timeout = self._normalize_timeout(timeout)
        pipe = self.client.pipeline(transaction=False)

        for key, value in mapping.items():
            dump = self.dump_object(value)
            if timeout == -1:
                pipe.set(name=self.key_prefix + key, value=dump)
            else:
                pipe.setex(
                    name=self.key_prefix + key, value=dump, time=timeout
                )
        return pipe.execute()
