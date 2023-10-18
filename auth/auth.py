from fastapi import APIRouter, HTTPException

from auth import account_util
from auth.dto.return_code import IdValidateCode, PWValidateCode
from core import sql_util

router = APIRouter()


@router.post("/register")
def register_user(id: str, pw: str):
    id_val_code = account_util.validate_id(id)
    if id_val_code != IdValidateCode.NON_EXIST_ID:
        return {"status": "fail", "code": id_val_code.name}
    pw_val_code = account_util.validate_pw(id, pw)
    if pw_val_code != PWValidateCode.SUCCESS:
        return {"status": "fail", "code": pw_val_code.name}
    user = sql_util.create_user(id, account_util.encode_pw(pw))
    if user is not None:
        jwt_token = account_util.calculate_jwt(user.jwtKey)
        return {"status": "success", "jwt": jwt_token}
    return {"status": "fail", "code": "UNKNOWN"}
