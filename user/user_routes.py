from typing import Annotated

from fastapi import APIRouter, Depends

from auth.auth_routes import oauth2_scheme
from auth.auth_tools import validate_jwt
from database.db_tools import db_get_salary_info

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/salary")
async def get_user_salary(token: Annotated[str, Depends((oauth2_scheme))]):
    payload = validate_jwt(token)
    salary_data = db_get_salary_info(payload.get("id"))
    if not salary_data:
        return None
    return salary_data.get("amnt")

@router.get("/salary/next_raise_dt")
async def get_user_salary_raise_dt(token: Annotated[str, Depends((oauth2_scheme))]):
    payload = validate_jwt(token)
    salary_data = db_get_salary_info(payload.get("id"))
    if not salary_data:
        return None
    return salary_data.get("next_raise_dt")