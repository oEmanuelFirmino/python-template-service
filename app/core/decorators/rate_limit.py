import time
from functools import wraps


def rate_limit(calls: int, period: float):
    def decorator(func):
        timestamps = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            while timestamps and timestamps[0] < now - period:
                timestamps.pop(0)

            if len(timestamps) >= calls:
                raise Exception("Rate limit exceeded")

            timestamps.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator