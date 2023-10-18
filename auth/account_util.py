import hashlib
import os
import re

import jwt

from auth.dto.return_code import IdValidateCode, PWValidateCode
from auth.rule import id_rule, pw_rule
from core import sql_util

_SALT = os.environ.get("AIT_PW_SALT")  # admin only
_PERPPER = os.environ.get("AIT_PW_PEPPER")  # admin only


def validate_id(id: str) -> IdValidateCode:
    if len(id) < id_rule.MIN_LENGTH:
        return IdValidateCode.ID_TOO_SHORT
    if len(id) > id_rule.MAX_LENGTH:
        return IdValidateCode.ID_TOO_LONG
    if is_include_not_allowed_char(id):
        return IdValidateCode.ID_NOT_ALLOWED_CHAR
    if len(re.findall(r"[0-9]", id)) < id_rule.MIN_NUMBER_LEN:
        return IdValidateCode.ID_REQ_NUMBER
    if len(re.findall(r"[A-z]", id)) < id_rule.MIN_CHAR_LEN:
        return IdValidateCode.ID_REQ_CHAR
    if re.search(r"(.)\1{" + str(id_rule.MAX_REPEAT_TIME) + ",}", id):
        return IdValidateCode.ID_TOO_SIMPLE
    if has_consecutive_char(id, id_rule.MAX_REPEAT_TIME):
        return IdValidateCode.ID_TOO_SIMPLE
    if sql_util.find_user(id) is not None:
        return IdValidateCode.ALREADY_EXIST_ID

    return IdValidateCode.SUCCESS


def validate_pw(id: str, pw: str) -> PWValidateCode:
    if len(pw) < pw_rule.MIN_LENGTH:
        return PWValidateCode.PW_TOO_SHOTR
    if len(pw) > pw_rule.MAX_LENGTH:
        return PWValidateCode.PW_TOO_LONG
    if is_include_not_allowed_char(pw):
        return PWValidateCode.PW_NOT_ALLOWED_CHAR
    if len(re.findall(r"[0-9]", pw)) < pw_rule.MIN_NUMBER_LEN:
        return PWValidateCode.PW_REQ_NUMBER
    if len(re.findall(r"[A-z]", pw)) < pw_rule.MIN_CHAR_LEN:
        return PWValidateCode.PW_REQ_CHAR
    if re.search(r"(.)\1{" + str(pw_rule.MAX_REPEAT_TIME - 1) + ",}"):
        return PWValidateCode.PW_TOO_SIMPLE
    if has_consecutive_char(pw, pw_rule.MAX_REPEAT_TIME):
        return PWValidateCode.PW_TOO_SIMPLE
    if is_similar_password(id, pw, pw_rule.MAX_ID_SIMILARITY + 1):
        return PWValidateCode.PW_TOO_SIMILAR_WITH_ID

    return PWValidateCode.SUCCESS


def encode_pw(pw: str):
    encoded_pw = str(hashlib.sha3_512((pw + _SALT).encode()).hexdigest())
    encoded_pw += _PERPPER
    return


def validate_jwt(jwt_token: str, id: str) -> bool:
    user = sql_util.find_user(id)
    if user == None:
        return False
    try:
        head = jwt.decode(jwt_token, user.jwtKey, algorithms="HS256")
        return True
    except:
        return False


def calculate_jwt(jwt_key: str):
    # JWT 헤더에 들어갈 데이터 결정
    jwt_token = jwt.encode({}, jwt_key, algorithm="HS256")
    return jwt_token


# 허용되지 않은 문자가 있는지만 검색
def is_include_not_allowed_char(input_str: str) -> bool:
    return not bool(id_rule.ALLOWED_CHAR_RE.fullmatch(input_str))


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


def is_similar_password(id: str, pw: str, count: int):
    for i in range(len(id) - count + 1):
        for j in range(len(pw) - count + 1):
            if id[i : i + count] == pw[j : j + count]:
                return True
    return False
