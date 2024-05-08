import datetime

import bcrypt
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, status

from config import SECRET_KEY, ALGORITHM, EXP_TIME_SEC

#----------------------------------------------------------------------------------------------------------------------------------------
# JWT get-check :

def create_jwt(
        payload: dict,
        key: str = SECRET_KEY,
        algorithm: str = ALGORITHM,
        exp_timedelta: int = EXP_TIME_SEC
) -> str:
    exp_datetime = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=exp_timedelta)
    data = payload.copy()
    data.update({"exp": exp_datetime})
    return jwt.encode(data, key, algorithm)

def validate_jwt(token: str, key: str = SECRET_KEY, algorithm: str = ALGORITHM):
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
    except PyJWTError as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid JWT"
        )
    return payload
#----------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------
# password encrypt-validation:

def create_pwd_hash(pwd: str) -> bytes:
    pwd_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return pwd_hash

def validate_pwd(pwd: str, pwd_hash: bytes):
    return bcrypt.checkpw(pwd.encode(), pwd_hash)
#----------------------------------------------------------------------------------------------------------------------------------------
