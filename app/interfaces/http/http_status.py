from enum import Enum


class HttpStatus(Enum):

    OK = (
        200,
        "OK",
        "Request completed successfully",
    )
    CREATED = (
        201,
        "Created",
        "Resource created successfully",
    )
    NO_CONTENT = (
        204,
        "No Content",
        "Operation completed successfully",
    )

    BAD_REQUEST = (
        400,
        "Bad Request",
        "Invalid request parameters",
    )
    UNAUTHORIZED = (
        401,
        "Unauthorized",
        "Authentication required or invalid credentials",
    )
    FORBIDDEN = (
        403,
        "Forbidden",
        "You don't have permission to access this resource",
    )
    NOT_FOUND = (
        404,
        "Not Found",
        "Resource not found",
    )
    CONFLICT = (
        409,
        "Conflict",
        "Resource already exists or conflict with current state",
    )

    INTERNAL_SERVER_ERROR = (
        500,
        "Internal Server Error",
        "Internal server error occurred",
    )

    def __init__(self, code: int, description: str, message: str):
        self.code = code
        self.description = description
        self.message = message

    @classmethod
    def error_responses(cls) -> dict:
        return {
            status.code: {
                "description": status.description,
                "content": {
                    "application/json": {"example": {"detail": status.message}}
                },
            }
            for status in cls
            if status.code >= 400
        }


error_responses = HttpStatus.error_responses()
