from enum import Enum


class ResponseStatus(Enum):
    fail = 0
    success = 1

    def __str__(self) -> str:
        return self.name


class Response:
    def __init__(self, status: ResponseStatus, data: dict):
        self.status = status
        self.data = data

    def __str__(self) -> str:
        keys = self.__dict__.keys()
        res = "Response:\n"
        for k in keys:
            res += "\t{}: {}\n".format(k, str(self.__dict__[k]))
        return res

    def __iter__(self):
        for key in self.__dict__:
            attr = getattr(self, key)
            if isinstance(attr, ResponseStatus):
                attr = attr.name
            yield key, attr
