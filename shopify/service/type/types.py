from enum import Enum

class ResponseType(Enum):
    NOT_FOUND = 404
    UNSAFE_ARGS = 403
    SUCCESS = 200
    INVALID_ARGS = 502
    SERVER_ERROR = 500