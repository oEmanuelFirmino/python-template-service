from functools import lru_cache
from typing import Type, TypeVar, Callable, Dict, Any

T = TypeVar("T")


class Container:
    _registry: Dict[Type[Any], Callable[[], Any]] = {}

    @classmethod
    def register(cls, key: Type[T], factory: Callable[[], T]) -> None:
        cls._registry[key] = lru_cache(factory)

    @classmethod
    def resolve(cls, key: Type[T]) -> T:
        if key not in cls._registry:
            raise ValueError(f"No provider registered for {key}")
        return cls._registry[key]()