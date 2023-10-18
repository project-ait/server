from datetime import datetime
from enum import Enum


class UserState(Enum):
    ACTIVATE = 0
    INACTIVATE = 1
    BANNED = 2

    def __str__(self) -> str:
        return self.name


class UserValidateState(Enum):
    VALIDATED = 0
    NOT_VALIDATE = 1
    PROGRESSING = 2

    def __str__(self) -> str:
        return self.name


class UserDto:
    def __init__(
        self,
        id: int,
        user_id: str,
        password: str,
        jwtKey: str,
        validState: str,
        state: str,
        registerTimestamp: datetime,
        validTimestamp: datetime,
        email: str,
    ):
        self.__init__(
            id,
            user_id,
            password,
            jwtKey,
            UserValidateState[validState],
            UserState[state],
            registerTimestamp,
            validTimestamp,
            email,
        )

    def __init__(
        self,
        id: int,
        user_id: str,
        password: str,
        jwtKey: str,
        validState: UserValidateState,
        state: UserState,
        registerTimestamp: datetime,
        validTimestamp: datetime,
        email: str,
    ):
        self.id = id
        self.user_id = user_id
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
            res += "\t{}: {}\n".format(k, str(self.__dict__[k]))
        return res
