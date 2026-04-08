from functools import lru_cache


def cache(maxsize: int = 128):
    def decorator(func):
        return lru_cache(maxsize=maxsize)(func)
    return decorator