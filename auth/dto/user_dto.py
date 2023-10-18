from datetime import datetime


class UserDto:
    def __init__(
        self,
        user_id: int,
        id: str,
        password: str,
        jwtKey: str,
        validState: str,
        state: str,
        registerTimestamp: datetime,
        validTimestamp: datetime,
        email: str,
    ):
        self.user_id = user_id
        self.id = id
        self.password = password
        self.jwtKey = jwtKey
        self.validState = validState
        self.state = state
        self.registerTimestamp = registerTimestamp
        self.validTimestamp = validTimestamp
        self.email = email

    def __str__(self) -> str:
        keys = self.__dict__.keys()
        res = "UserDto:\n"
        for k in keys:
            res += "\t{}: {}\n".format(k, self.__dict__[k])
        return res
