import time
from functools import wraps
from typing import Callable, Any

from core.logger import get_logger


def log_execution(step: str | None = None):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        logger = get_logger(func.__module__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start

                logger.info(
                    f"{func.__name__} executed in {duration:.4f}s",
                    extra={
                        "step": step or func.__name__,
                        "document_id": kwargs.get("document_id", "-"),
                    },
                )

                return result

            except Exception as e:
                duration = time.time() - start

                logger.error(
                    f"{func.__name__} failed after {duration:.4f}s: {e}",
                    extra={
                        "step": step or func.__name__,
                        "document_id": kwargs.get("document_id", "-"),
                    },
                )
                raise

        return wrapper

    return decorator