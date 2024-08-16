#!/usr/bin/env python3
"provides the Cache class"
import redis
import uuid
from typing import Union


class Cache:
    "Cache class"
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        "store method"
        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key
