#!/usr/bin/env python3
"""provides the Cache class"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count_calls decorator"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper method"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """call_history method"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper method"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def replay(method: Callable) -> Callable:
    """replay method"""
    r_inst = method.__self__._redis
    key = method.__qualname__

    inputs_key = f"{key}:inputs"
    outputs_key = f"{key}:outputs"

    inputs = r_inst.lrange(inputs_key, 0, -1)
    outputs = r_inst.lrange(outputs_key, 0, -1)

    print("{} was called {} times".format(method.__qualname__, len(inputs)))
    for input, output in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, input.decode("utf-8"), output.decode("utf-8")
            )
        )


class Cache:
    """Cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method"""
        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """get method"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """get_str method"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """get_int method"""
        return self.get(key, fn=int)
