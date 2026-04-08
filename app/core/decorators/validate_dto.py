from functools import wraps
from pydantic import BaseModel


def validate_dto(dto_class: type[BaseModel]):
    def decorator(func):
        @wraps(func)
        def wrapper(data, *args, **kwargs):
            validated = dto_class.model_validate(data)
            return func(validated, *args, **kwargs)

        return wrapper
    return decorator