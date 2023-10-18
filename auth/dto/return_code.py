from enum import Enum


class IdValidateCode(Enum):
    ALREADY_EXIST_ID = 0
    ID_TOO_SHORT = 1
    ID_TOO_LONG = 2
    ID_NOT_ALLOWED_CHAR = 3
    ID_REQ_NUMBER = 4
    ID_REQ_CHAR = 5
    ID_TOO_SIMPLE = 6
    NON_EXIST_ID = 7


class PWValidateCode(Enum):
    PW_TOO_SHORT = 0
    PW_TOO_LONG = 1
    PW_NOT_ALLOWED_CHAR = 2
    PW_REQ_NUMBER = 3
    PW_REQ_CHAR = 4
    PW_TOO_SIMILAR_WITH_ID = 5
    PW_TOO_SIMPLE = 6
    SUCCESS = 7


class JWTValidateCode(Enum):
    UNAUTHORIZED = 0
    NON_EXIST_USER = 1
    EXPIRED_TOKEN = 2
    AUTHORIZED = 3
