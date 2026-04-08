from typing import Callable, get_type_hints
from fastapi import Depends

from api.container import Container


def inject(func: Callable) -> Callable:
    hints = get_type_hints(func)

    dependencies = {
        name: Depends(lambda t=typ: Container.resolve(t))
        for name, typ in hints.items()
        if typ in Container._registry
    }

    for name, dep in dependencies.items():
        func.__annotations__[name] = dep

    return func