from fastapi import Request, Response, HTTPException
from jwt import ExpiredSignatureError, InvalidAlgorithmError, InvalidTokenError
from app.core.settings import settings
from app.core.jwt_handle import verify_token
from typing import Optional
# JWT토큰을 쿠키로 설정하려고
# Httponly=True : 쿠키를 만들면 js에서 접근 불가(xss공격방어)
def set_auth_cookies(response:Response,access_token:str, refresh_token:str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=int(settings.access_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=int(settings.refresh_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite="Lax",
    )

# 사용자 쿠키에 액세스 토큰있는지 확인
async def get_user_id(request:Request) -> int:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access_token missing")
    
    try:
        user_id=verify_token(access_token)
        if user_id is None:
            raise HTTPException(status_code=401, detail="no uid")
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail= "Access_token expired")
    except InvalidAlgorithmError:
        raise HTTPException(status_code=401, detail="Invalid Access_token")

async def get_optional(request:Request) -> Optional[int]:
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    try:
        return verify_token(access_token)
    except(ExpiredSignatureError,InvalidTokenError):
        return None