#!/usr/bin/env python3
"""provides the Cache class"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """Cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method"""
        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(self, key: str, fn: Optional[Callable]=None) -> Union[str, bytes, int, float, None]:
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
