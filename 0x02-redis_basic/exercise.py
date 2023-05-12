#!/usr/bin/env python3
"""
Learning how to use redis for basic operations
and as a simple cache
"""
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    A decorator function that counts how many
    times methods of the Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator function that will add its input parameters
    to one list in redis, and store its output into another list.
    """
    key_prefix = method.__qualname__
    print('prefix:', key_prefix)

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for decorated function"""
        inputs_key = f'{key_prefix}:inputs'
        outputs_key = f'{key_prefix}:outputs'

        inputs = str(args)
        self._redis.rpush(inputs_key, inputs)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(outputs_key, output)

        return output

    return wrapper


def replay(fn: Callable):
    """A function that displays the history
    of calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    # print(f"{function_name} was called {value} times:")
    print("{} was called {} times:".format(function_name, value))
    # inputs = r.lrange(f"{function_name}:inputs", 0, -1)
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    # outputs = r.lrange(f"{function_name}:outputs", 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        # print(f"{function_name}(*{input}) -> {output}")
        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """A Cache class"""

    def __init__(self):
        """Ïnitialises an instance of Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[int, float, str, bytes]) -> str:
        """
        A method that stores the input data in Redis using a random key
        and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        A method that takes a key string argument
        and an optional Callable argument named fn.
        This callable will be used to convert
        the data back to the desired format.
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
        except Exception:
            return 0

        return val
