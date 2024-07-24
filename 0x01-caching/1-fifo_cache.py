#!/usr/bin/env python3
"""This if FIFO caching module.
"""
from collections import OrderedDict

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """fetchs the item that enables storing to
    get objecs in the dictionary from a FIFO
    purging methods if the limit is reached.
    """
    def __init__(self):
        """sets up the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """appends an object into cache.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", first_key)

    def get(self, key):
        """fetchs an object by its key.
        """
        return self.cache_data.get(key, None)
