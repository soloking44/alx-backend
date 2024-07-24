#!/usr/bin/env python3
"""this is LFU caching module.
"""
from collections import OrderedDict

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """shows the item that enables storing to
    get objects in a dictionary into a LFU
    purging methods if limit are reached.
    """
    def __init__(self):
        """sets up a cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.keys_freq = []

    def __reorder_items(self, mru_key):
        """Resets objects into a cache reliant into
        currently used object.
        """
        max_positions = []
        mru_freq = 0
        mru_pos = 0
        ins_pos = 0
        for k, key_freq in enumerate(self.keys_freq):
            if key_freq[0] == mru_key:
                mru_freq = key_freq[1] + 1
                mru_pos = k
                break
            elif len(max_positions) == 0:
                max_positions.append(k)
            elif key_freq[1] < self.keys_freq[max_positions[-1]][1]:
                max_positions.append(k)
        max_positions.reverse()
        for pos in max_positions:
            if self.keys_freq[pos][1] > mru_freq:
                break
            ins_pos = pos
        self.keys_freq.pop(mru_pos)
        self.keys_freq.insert(ins_pos, [mru_key, mru_freq])

    def put(self, key, item):
        """appends object in a cache.
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                lfu_key, _ = self.keys_freq[-1]
                self.cache_data.pop(lfu_key)
                self.keys_freq.pop()
                print("DISCARD:", lfu_key)
            self.cache_data[key] = item
            ins_index = len(self.keys_freq)
            for k, key_freq in enumerate(self.keys_freq):
                if key_freq[1] == 0:
                    ins_index = k
                    break
            self.keys_freq.insert(ins_index, [key, 0])
        else:
            self.cache_data[key] = item
            self.__reorder_items(key)

    def get(self, key):
        """fetchs the object by its key.
        """
        if key is not None and key in self.cache_data:
            self.__reorder_items(key)
        return self.cache_data.get(key, None)
