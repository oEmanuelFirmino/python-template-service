from typing import Callable, TypeVar

T = TypeVar("T")


def resolve(factory: Callable[[], T]) -> Callable[[], T]:
    return factory