import datetime
import hashlib
import os
import typing

import sqlite3

from oauth.dto.user_dto import UserDto


def env(key):
    return os.environ.get(key)


_DIR = "./database.sqlite"
_IS_TEST = env("IS_TEST")


_conn = sqlite3.connect(_DIR) if not _IS_TEST else None


def check_and_create_table():
    print("Checking Table...")
    table = "account"
    cmd = _conn.cursor()
    cmd.execute(
        """
        CREATE TABLE IF NOT EXISTS {} (
            id SERIAL PRIMARY KEY,
            "userId" character varying(20) NOT NULL UNIQUE,
            password character varying(256) NOT NULL,
            "jwtKey" character varying(128) NOT NULL,
            "validState" character varying(20) NOT NULL,
            state character varying(20) NOT NULL,
            "registerTimestamp" timestamp without time zone NOT NULL,
            "validTimestamp" timestamp without time zone,
            email character varying(30)
        )
        """.format(
            table
        )
    )
    _conn.commit()
    cmd.close()


def create_user(_id: str, encoded_pw: str) -> typing.Union[UserDto, None]:
    table = "account"
    jwt_key = str(hashlib.sha3_512((_id + "/" + encoded_pw).encode()).hexdigest())
    valid_state = "NOT_VALID"
    state = "ACTIVATE"
    register_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cmd = _conn.cursor()
    try:
        cmd.execute(
            "INSERT INTO {} ({}) VALUES ({})".format(
                table,
                '"userId", password, "jwtKey", "validState", state, "registerTimestamp"',
                "'{}', '{}', '{}', '{}', '{}', '{}'".format(
                    _id,
                    encoded_pw,
                    jwt_key,
                    valid_state,
                    state,
                    register_timestamp,
                ),
            )
        )
        user = find_user(_id)
        _conn.commit()
        return user
    except:
        return None
    finally:
        cmd.close()


def find_user(_id: str) -> typing.Union[UserDto, None]:
    table = "account"
    cmd = _conn.cursor()
    cmd.execute(
        "SELECT * FROM {} WHERE \"userId\"='{}' limit 1".format(
            table,
            _id,
        )
    )
    rec = cmd.fetchone()
    cmd.close()
    if rec is not None:
        return UserDto(*rec)
    return None


def delete_user(_id: str) -> bool:
    table = "account"
    cmd = _conn.cursor()
    try:
        cmd.execute(
            'DELETE FROM {} WHERE "userId"={}'.format(
                table,
                _id,
            )
        )
        _conn.commit()
        return True
    except:
        return False
    finally:
        cmd.close()
