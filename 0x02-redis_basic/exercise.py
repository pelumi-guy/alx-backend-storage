#!/usr/bin/env python3
"""
Learning how to use redis for basic operations
and as a simple cache
"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:

    def __init__(self):
        """Ïnitialises an instance of Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data : Union[int , float , str , bytes]) -> str:
        """
        A method that stores the input data in Redis using a random key
        and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        A method that takes a key string argument and an optional Callable argument named fn.
        This callable will be used to convert the data back to the desired format.
        """
        ret = self._redis.get(key)
        if ret and fn:
            ret = fn(ret)

        return ret

    def get_str(self, key: str):
        """
        A method that automatically parametrize Cache.get to return a string
        """
        ret = self.get(key)

        return ret.decode('utf8')

    def get_int(self, key: str):
        """
        A method that automatically parametrize Cache.get to return an integer
        """
        ret = self.get(key)

        try:
            val = int(ret.decode('utf8'))
        except:
            return 0

        return val
