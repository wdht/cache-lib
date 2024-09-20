class BaseCache:
    def __init__(self, default_timeout=300):
        self.default_timeout = default_timeout

    def _normalize_timeout(self, timeout):
        if timeout is None:
            timeout = self.default_timeout
        return timeout

    def get(self, key):
        """Look up key in the cache and return the value for it."""
        return None

    def get_many(self, *keys):
        """Returns a list of values for the given keys."""
        return [self.get(k) for k in keys]

    def get_dict(self, *keys):
        """Return values mapped to keys"""
        return dict(zip(keys, self.get_many(*keys)))

    def set(self, key, value, timeout=None):
        """
        Add a new key/value to the cache (overwrites value, if key already
        exists in the cache).
        """
        return True

    def set_many(self, mapping, timeout=None):
        """Sets multiple keys and values from a mapping."""
        return_value = True
        for key, value in mapping.items():
            if not self.set(key, value, timeout):
                return_value = False
        return return_value
