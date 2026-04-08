from typing import Type, TypeVar, Callable
from api.container import Container

T = TypeVar("T")


def get_dependency(dep: Type[T]) -> Callable[[], T]:
    def _get() -> T:
        return Container.resolve(dep)
    return _get