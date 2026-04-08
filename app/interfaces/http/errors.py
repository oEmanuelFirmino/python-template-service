from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: int
    message: str
    context: dict | None = None