#!/usr/bin/env python3
"""this is MRU caching module.
"""
from collections import OrderedDict

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """shows an item that enables storing to
    get objects in a dictionary in MRU
    purging methods if a limit are reached.
    """
    def __init__(self):
        """sets up a cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """appends object into a cache.
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                mru_key, _ = self.cache_data.popitem(False)
                print("DISCARD:", mru_key)
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=False)
        else:
            self.cache_data[key] = item

    def get(self, key):
        """fetchs the object by its key.
        """
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key, None)
