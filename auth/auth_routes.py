from typing import Annotated

from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel

from auth.auth_tools import create_jwt, validate_pwd
from database.db_tools import db_get_user_pwd

#----------------------------------------------------------------------------------------------------------------------------------------
router = APIRouter(tags=["Auth JWT"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/auth")
async def auth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid user credentials"
    )
    user = db_get_user_pwd(form_data.username)
    if not user:
        raise auth_exp
    if not validate_pwd(form_data.password, user.get("pwd")):
        raise auth_exp
    jwt_token = create_jwt({"id": form_data.username})
    return Token(access_token = jwt_token, token_type = "bearer")
#----------------------------------------------------------------------------------------------------------------------------------------

