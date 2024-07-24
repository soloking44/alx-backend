#!/usr/bin/env python3
"""This is basic caching module.
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """shows item that enables storing to
    fetch objects in the dictionary.
    """
    def put(self, key, item):
        """Adds an item in the cache.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """fetchs the object with its key.
        """
        return self.cache_data.get(key, None)
