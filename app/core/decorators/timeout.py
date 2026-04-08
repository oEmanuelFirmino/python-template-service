import signal
from functools import wraps


def timeout(seconds: int):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError(f"{func.__name__} timed out")

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)

        return wrapper

    return decorator