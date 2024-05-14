import httpx

from tests.conftest import API_URL

AUTH_URL = f"{API_URL}/auth"
AUTH_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

def test_auth_valid_login():
    auth_data = {
        "username": "e0001",
        "password": 1,
    }
    request = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert request.status_code == 200
    assert "access_token" in request.json() and "token_type" in request.json() and request.json()["token_type"] == "bearer"

def test_auth_invalid_login():
    auth_data = {
        "username": "fake",
        "password": 1,
    }
    request = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert request.status_code == 401
    assert request.json()["detail"] == "Invalid user credentials"

def test_auth_invalid_password():
    auth_data = {
        "username": "e0001",
        "password": "fake",
    }
    request = httpx.post(url=AUTH_URL, headers=AUTH_HEADERS, data=auth_data)
    assert request.status_code == 401
    assert request.json()["detail"] == "Invalid user credentials"

