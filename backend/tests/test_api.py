import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000"


def test_root():
    response = httpx.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI"}


@pytest.mark.parametrize(
    ("headers", "message"),
    [
        ({}, "Not authenticated"),
        ({"Authorization": "Bearer not-a-jwt"}, "会话失效，请重新登录"),
    ],
    ids=["missing-token", "invalid-token"],
)
def test_user_info_rejects_unauthenticated_requests(headers, message):
    response = httpx.get(f"{BASE_URL}/api/user/info", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"code": 401, "message": message, "data": None}


@pytest.mark.parametrize("username", ["s1", "nonexistent-api-test-user"])
def test_login_rejects_wrong_credentials(username):
    response = httpx.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": username, "password": "invalid-test-password"},
    )
    assert response.status_code == 200  # ServiceException 使用业务码
    assert response.json() == {
        "code": 500,
        "message": "Wrong account or password",
        "data": None,
    }


@pytest.mark.parametrize("payload", [{"username": "s1"}, {"password": "s1"}])
def test_login_requires_both_fields(payload):
    response = httpx.post(f"{BASE_URL}/api/auth/login", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["code"] == 422
    assert isinstance(body["message"], str) and body["message"]
    assert body["data"] is None


def test_login_then_get_user_info():
    login = httpx.post(
        f"{BASE_URL}/api/auth/login", json={"username": "s1", "password": "s1"}
    )

    assert login.status_code == 200
    body = login.json()
    assert body["code"] == 200, body["message"]
    token = body["data"]["token"]

    # with jwt token
    info = httpx.get(
        f"{BASE_URL}/api/user/info", headers={"Authorization": f"Bearer {token}"}
    )

    assert info.status_code == 200
    body = info.json()
    assert body["code"] == 200
    assert body["data"]["username"] == "s1"
    assert body["data"]["role"] == "student"
    assert body["data"]["status"] == 1
    assert body["data"] == login.json()["data"]["user"]
    assert "password" not in body["data"]
