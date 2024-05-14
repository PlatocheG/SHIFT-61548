import time

import httpx
import pytest

from config import JWT_EXP_TIME_SEC
from tests.conftest import API_URL


AUTH_URL = f"{API_URL}/auth"
AUTH_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}
USER_SALARY_URL = f"{API_URL}/user/salary"
SALARY_NEXT_RAISE_URL = f"{API_URL}/user/salary/next_raise_dt"

def user_salary_headers(jwt):
    user_salary_headers = {
        "accept": "application/json",
        "Authorization": f"{jwt.json()["token_type"]} {jwt.json()["access_token"]}"
    }
    return user_salary_headers

def test_user_salary():
    auth_data = {
        "username": "e0001",
        "password": 1,
    }
    jwt = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert jwt.status_code == 200
    salary_response = httpx.get(url=USER_SALARY_URL, headers=user_salary_headers(jwt))
    assert salary_response.json() == 1

def test_user_salary_null_val():
    auth_data = {
        "username": "e0003",
        "password": 3,
    }
    jwt = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert jwt.status_code == 200
    salary_response = httpx.get(url=USER_SALARY_URL, headers=user_salary_headers(jwt))
    assert salary_response.json() == None

def test_salary_next_raise():
    auth_data = {
        "username": "e0001",
        "password": 1,
    }
    jwt = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert jwt.status_code == 200
    salary_response = httpx.get(url=SALARY_NEXT_RAISE_URL, headers=user_salary_headers(jwt))
    assert salary_response.json() == "2027-01-01 00:00:00"

def test_salary_next_raise_null_val():
    auth_data = {
        "username": "e0003",
        "password": 3,
    }
    jwt = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert jwt.status_code == 200
    salary_response = httpx.get(url=SALARY_NEXT_RAISE_URL, headers=user_salary_headers(jwt))
    assert salary_response.json() == None

def test_user_invalid_jwt():
    fake_user_jwt = {
        "accept": "application/json",
        "Authorization": f"Bearer fake.jwt.key"
    }
    salary_response = httpx.get(url=SALARY_NEXT_RAISE_URL, headers=fake_user_jwt)
    assert salary_response.status_code == 401
    assert salary_response.json() == {'detail': 'Invalid JWT'}



@pytest.mark.skipif('config.getoption("--test") == "fast"')
def test_user_jwt_expiration():
    auth_data = {
        "username": "e0001",
        "password": 1,
    }
    jwt = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert jwt.status_code == 200
    time.sleep(JWT_EXP_TIME_SEC + 1)
    salary_response = httpx.get(url=USER_SALARY_URL, headers=user_salary_headers(jwt))
    assert salary_response.status_code == 401
    assert salary_response.json() == {'detail': 'Invalid JWT'}