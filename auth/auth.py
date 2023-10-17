from fastapi import APIRouter, HTTPException

from auth import account_util, account_validation
from auth.dto.return_code import IdValidateCode, PWValidateCode
from core import sql_util

router = APIRouter()


@router.post("/register")
def register_user(id: str, pw: str):
    id_val_code = account_util.validate_id(id)
    if id_val_code != IdValidateCode.SUCCESS:
        return {"status": "fail", "code": id_val_code}
    pw_val_code = account_util.validate_pw(pw)
    if pw_val_code != PWValidateCode.SUCCESS:
        return {"status": "fail", "code": pw_val_code}
    user = sql_util.create_user(id, account_util.encode_pw(pw))
    if user is not None:
        jwt_token = account_util.calculate_jwt(user.jwtKey)
        return {"status": "success", "jwt": jwt_token}
    return {"status": "fail", "code": "UNKNOWN"}
