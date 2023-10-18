import datetime
import hashlib
import os

import psycopg2
from psycopg2 import connection

from auth.dto.user_dto import UserDto

_HOST = "localhost"
_PORT = 5432
_USER = os.environ.get("AIT_DB_USER")
_PW = os.environ.get("AIT_DB_PW")
_DATABASE = os.environ.get("AIT_DB_NAME")

_IS_TEST = os.environ.get("IS_TEST")

if not _IS_TEST:
    if _USER is None:
        raise Exception("DB 접속 유저 이름이 설정되지 않았습니다")
    if _PW is None:
        raise Exception("DB 접속 암호가 설정되지 않았습니다")
    if _DATABASE is None:
        raise Exception("접속할 DB 이름을 설정하지 않았습니다")

_conn: connection = psycopg2.connect(
    host=_HOST,
    dbname=_DATABASE,
    user=_USER,
    password=_PW,
    port=_PORT,
) if not _IS_TEST else None


def create_user(id: str, encoded_pw: str) -> UserDto:
    table = "account"
    jwt_key = str(hashlib.sha3_512((id + "/" + encoded_pw).encode()).hexdigest())
    valid_state = "NOT_VALID"
    state = "ACTIVATE"
    register_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn.cursor() as cmd:
        try:
            cmd.execute(
                "INSERT INTO {} ({}) VALUES ({})".format(
                    table,
                    '"userId", password, "jwtKey", "validState", state, "registerTimestamp"',
                    "'{}', '{}', '{}', '{}', '{}', '{}'".format(
                        id,
                        encoded_pw,
                        jwt_key,
                        valid_state,
                        state,
                        register_timestamp,
                    ),
                )
            )
            user = find_user(id)
            _conn.commit()
            return user
        except Exception as e:
            print(e)
            return None


def find_user(id: str) -> UserDto:
    table = "account"
    with _conn.cursor() as cmd:
        cmd.execute(
            "SELECT * FROM {} WHERE \"userId\"='{}' limit 1".format(
                table,
                id,
            )
        )
        rec = cmd.fetchone()
        if rec is not None:
            return UserDto(*rec)
