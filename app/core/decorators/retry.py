import time
from functools import wraps
from typing import Callable, Type


def retry(
    retries: int = 3,
    delay: float = 0.5,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    time.sleep(delay)

            raise last_error

        return wrapper

    return decorator