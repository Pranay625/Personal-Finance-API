from datatime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "Gaara"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datatime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm = ALGORITHM
    )

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithm=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code = 401,
                detail = "Invalid token"
            )
        
        return username

    except JWTError:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid or expired token"
        )

def get_current_user(
        token: str = Depends(oauth2_scheme)
    
):
    return verify_token(token)