import hashlib
import os
import re
from datetime import datetime, timedelta

import jwt

from core import sql_util
from service.oauth.dto.return_code import (
    IdValidateCode as IdValid,
    PWValidateCode as PwValid,
    JWTValidateCode as JWTValid
)
from service.oauth.rule.id_rule import ALLOWED_CHAR_RE

_SALT = os.environ.get("AIT_PW_SALT")  # admin only
_PEPPER = os.environ.get("AIT_PW_PEPPER")  # admin only


# noinspection DuplicatedCode
def validate_id(_id: str) -> IdValid:
    from service.oauth.rule.id_rule import (
        MAX_LENGTH, MIN_LENGTH,
        MIN_CHAR_LEN, MIN_NUMBER_LEN,
        MAX_REPEAT_TIME
    )

    if len(_id) < MIN_LENGTH:
        return IdValid.ID_TOO_SHORT
    if len(_id) > MAX_LENGTH:
        return IdValid.ID_TOO_LONG
    if is_include_not_allowed_char(_id):
        return IdValid.ID_NOT_ALLOWED_CHAR
    if len(re.findall(r"[0-9]", _id)) < MIN_NUMBER_LEN:
        return IdValid.ID_REQ_NUMBER
    if len(re.findall(r"[A-z]", _id)) < MIN_CHAR_LEN:
        return IdValid.ID_REQ_CHAR
    if re.search(r"(.)\1{" + str(MAX_REPEAT_TIME) + ",}", _id):
        return IdValid.ID_TOO_SIMPLE
    if has_consecutive_char(_id, MAX_REPEAT_TIME):
        return IdValid.ID_TOO_SIMPLE

    # if sql_util.find_user(id) is not None:
    #     return IdValid.ALREADY_EXIST_ID

    return IdValid.NON_EXIST_ID


# noinspection DuplicatedCode
def validate_pw(_id: str, pw: str) -> PwValid:
    from service.oauth.rule.pw_rule import (
        MAX_LENGTH, MIN_LENGTH,
        MIN_CHAR_LEN, MIN_NUMBER_LEN,
        MAX_REPEAT_TIME, MAX_ID_SIMILARITY
    )

    if len(pw) < MIN_LENGTH:
        return PwValid.PW_TOO_SHORT
    if len(pw) > MAX_LENGTH:
        return PwValid.PW_TOO_LONG
    if is_include_not_allowed_char(pw):
        return PwValid.PW_NOT_ALLOWED_CHAR
    if len(re.findall(r"[0-9]", pw)) < MIN_NUMBER_LEN:
        return PwValid.PW_REQ_NUMBER
    if len(re.findall(r"[A-z]", pw)) < MIN_CHAR_LEN:
        return PwValid.PW_REQ_CHAR
    if re.search(r"(.)\1{" + str(MAX_REPEAT_TIME - 1) + ",}", pw):
        return PwValid.PW_TOO_SIMPLE
    if has_consecutive_char(pw, MAX_REPEAT_TIME):
        return PwValid.PW_TOO_SIMPLE
    if is_similar_password(_id, pw, MAX_ID_SIMILARITY + 1):
        return PwValid.PW_TOO_SIMILAR_WITH_ID

    return PwValid.SUCCESS


def encode_pw(pw: str) -> str:
    encoded_pw = str(hashlib.sha3_512((pw + _SALT).encode()).hexdigest())
    encoded_pw += _PEPPER
    return encoded_pw


def validate_jwt(jwt_token: str, _id: str) -> JWTValid:
    user = sql_util.find_user(_id)
    if user is None:
        return JWTValid.NON_EXIST_USER
    try:
        head = jwt.decode(jwt_token.encode(), user.jwtKey, algorithms="HS256")
        now = datetime.now().timestamp()
        if now > head["exp"]:
            return JWTValid.EXPIRED_TOKEN
        return JWTValid.AUTHORIZED
    except:
        return JWTValid.UNAUTHORIZED


def calculate_jwt(jwt_key: str) -> str:
    iat: datetime = datetime.now()
    exp: datetime = iat + timedelta(days=4)
    jwt_token = jwt.encode(
        {
            "iat": iat.timestamp(),
            "exp": exp.timestamp(),
        },
        jwt_key,
        algorithm="HS256",
    )
    return jwt_token


# 허용되지 않은 문자가 있는지만 검색
def is_include_not_allowed_char(input_str: str) -> bool:
    return not bool(ALLOWED_CHAR_RE.fullmatch(input_str))


# 1234, dcba 등 연속된 문자가 있는지 확인
def has_consecutive_char(input_str: str, count: int) -> bool:
    consecutive_count = 1
    increasing = decreasing = False  # 1212 등 오르내리는 경우 처리하기 위한 변수
    for i in range(1, len(input_str)):
        if not decreasing and ord(input_str[i]) == ord(input_str[i - 1]) + 1:
            consecutive_count += 1
            increasing = True
        elif not increasing and ord(input_str[i]) == ord(input_str[i - 1]) - 1:
            consecutive_count += 1
            decreasing = True
        else:
            consecutive_count = 1
            increasing = decreasing = False
        if consecutive_count > count:
            return True
    return False


def is_similar_password(_id: str, pw: str, count: int):
    for i in range(len(_id) - count + 1):
        for j in range(len(pw) - count + 1):
            if _id[i: i + count] == pw[j: j + count]:
                return True
    return False
