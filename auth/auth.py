from fastapi import APIRouter, HTTPException

from auth import account_util
from auth.dto.return_code import IdValidateCode, PWValidateCode
from core import sql_util
from core.response import Response, ResponseStatus

router = APIRouter()


@router.post("/register")
def register_user(id: str, pw: str):
    id_val_code = account_util.validate_id(id)
    if id_val_code != IdValidateCode.NON_EXIST_ID:
        return Response(
            ResponseStatus.fail,
            {"code": IdValidateCode.name},
        )
    pw_val_code = account_util.validate_pw(id, pw)
    if pw_val_code != PWValidateCode.SUCCESS:
        return Response(
            ResponseStatus.fail,
            {"code": pw_val_code.name},
        )
    user = sql_util.create_user(id, account_util.encode_pw(pw))
    if user is not None:
        jwt_token = account_util.calculate_jwt(user.jwtKey)
        return Response(
            ResponseStatus.success,
            {"jwt": jwt_token},
        )
    return Response(
        ResponseStatus.fail,
        {"code": "UNKNOWN"},
    )


@router.post("/login")
def login(id: str, pw: str):
    id_val_code = account_util.validate_id(id)
    if id_val_code != IdValidateCode.ALREADY_EXIST_ID:
        return Response(
            ResponseStatus.fail,
            {"code": id_val_code.name},
        )
    pw_val_code = account_util.validate_pw(id, pw)
    if pw_val_code != PWValidateCode.SUCCESS:
        return Response(
            ResponseStatus.fail,
            {"code": pw_val_code.name},
        )

    user = sql_util.find_user(id)
    encoded_pw = account_util.encode_pw(pw)
    if encoded_pw != user.password:
        return Response(
            ResponseStatus.fail,
            {"code": "INCORRECT_PW"},
        )
    jwt_token = account_util.calculate_jwt(user.jwtKey)
    return Response(
        ResponseStatus.success,
        {"jwt": jwt_token},
    )
