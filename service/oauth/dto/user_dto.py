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
            _id: int,
            user_id: str,
            password: str,
            jwt_key: str,
            valid_state: UserValidateState,
            state: UserState,
            register_timestamp: datetime,
            valid_timestamp: datetime,
            email: str,
    ):
        self._init_field(
            _id,
            user_id,
            password,
            jwt_key,
            valid_state,
            state,
            register_timestamp,
            valid_timestamp,
            email,
        )

    def _init_field(
            self,
            _idx: int,
            user_id: str,
            password: str,
            jwt_key: str,
            valid_state: UserValidateState,
            state: UserState,
            register_timestamp: datetime,
            valid_timestamp: datetime,
            email: str,
    ) -> None:
        self.id = _idx
        self.user_id = user_id
        self.password = password
        self.jwtKey = jwt_key
        self.validState = valid_state
        self.state = state
        self.registerTimestamp = register_timestamp
        self.validTimestamp = valid_timestamp
        self.email = email

    def __str__(self) -> str:
        keys = self.__dict__.keys()
        res = "UserDto:\n"
        for k in keys:
            res += "\t{}: {}\n".format(k, str(self.__dict__[k]))
        return res
