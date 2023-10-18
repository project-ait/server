from enum import Enum


class ResponseStatus(Enum):
    fail = 0
    success = 1


class Response:
    def __init__(self, status: ResponseStatus, data: dict):
        self.status = status
        self.data = data

    def __str__(self) -> str:
        return str(self.__dict__)

    def __iter__(self):
        for key in self.__dict__:
            attr = getattr(self, key)
            if isinstance(attr, Enum):
                return key, attr.name
            return key, attr
