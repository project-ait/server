from fastapi import APIRouter

from core import sql_util
from core.response import Response, ResponseStatus
from service.oauth.account_util import calculate_jwt, encode_pw, validate_pw, validate_id, validate_jwt
from service.oauth.dto.return_code import IdValidateCode, PWValidateCode, JWTValidateCode

router = APIRouter()


# noinspection DuplicatedCode
@router.post("/register", response_model=None)
def register_user(_id: str, pw: str) -> Response:
    id_val_code = validate_id(_id)
    if id_val_code != IdValidateCode.NON_EXIST_ID:
        return Response(
            ResponseStatus.fail,
            {"code": id_val_code.name},
        )

    pw_val_code = validate_pw(_id, pw)
    if pw_val_code != PWValidateCode.SUCCESS:
        return Response(
            ResponseStatus.fail,
            {"code": pw_val_code.name},
        )

    user = sql_util.create_user(_id, encode_pw(pw))
    if user is not None:
        jwt_token = calculate_jwt(user.jwtKey)
        return Response(
            ResponseStatus.success,
            {"jwt": jwt_token},
        )

    return Response(
        ResponseStatus.fail,
        {"code": "UNKNOWN"},
    )


# noinspection DuplicatedCode
@router.post("/login", response_model=None)
def login(_id: str, pw: str) -> Response:
    id_val_code = validate_id(_id)
    if id_val_code != IdValidateCode.ALREADY_EXIST_ID:
        return Response(
            ResponseStatus.fail,
            {"code": id_val_code.name},
        )

    pw_val_code = validate_pw(_id, pw)
    if pw_val_code != PWValidateCode.SUCCESS:
        return Response(
            ResponseStatus.fail,
            {"code": pw_val_code.name},
        )

    user = sql_util.find_user(_id)
    encoded_pw = encode_pw(pw)
    if encoded_pw != user.password:
        return Response(
            ResponseStatus.fail,
            {"code": "INCORRECT_PW"},
        )

    jwt_token = calculate_jwt(user.jwtKey)

    return Response(
        ResponseStatus.success,
        {"jwt": jwt_token},
    )


@router.post("/unregister", response_model=None)
def unregister(_id: str, jwt_token: str) -> Response:
    jwt_val_code = validate_jwt(jwt_token, _id)
    if jwt_val_code != JWTValidateCode.AUTHORIZED:
        return Response(
            ResponseStatus.fail,
            {"code": jwt_val_code.name},
        )

    if not sql_util.delete_user(_id):
        return Response(
            ResponseStatus.fail,
            {"code": "UNKNOWN_ERROR"},
        )

    return Response(
        ResponseStatus.success,
        {"msg": "DELETE SUCCESS"},
    )
