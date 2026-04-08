import tracemalloc
from functools import wraps
from typing import Callable, Any

from core.logger import get_logger


def measure_memory(step: str | None = None):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        logger = get_logger(func.__module__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()

            try:
                result = func(*args, **kwargs)

                current, peak = tracemalloc.get_traced_memory()

                logger.info(
                    f"{func.__name__} memory usage",
                    extra={
                        "step": step or func.__name__,
                        "document_id": kwargs.get("document_id", "-"),
                    },
                )

                logger.debug(
                    f"{func.__name__} memory stats: current={current / 10**6:.2f}MB, peak={peak / 10**6:.2f}MB",
                    extra={
                        "step": step or func.__name__,
                        "document_id": kwargs.get("document_id", "-"),
                    },
                )

                return result

            except Exception as e:
                current, peak = tracemalloc.get_traced_memory()

                logger.error(
                    f"{func.__name__} failed with memory peak={peak / 10**6:.2f}MB: {e}",
                    extra={
                        "step": step or func.__name__,
                        "document_id": kwargs.get("document_id", "-"),
                    },
                )
                raise

            finally:
                tracemalloc.stop()

        return wrapper

    return decorator