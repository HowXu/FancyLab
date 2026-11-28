from secrets import token_hex, token_urlsafe

import httpx
import pytest
from sqlalchemy import delete, update

from app.database import SessionLocal, engine
from app.models.user import User
from app.utils.password import hash_password


@pytest.fixture
def api():
    with httpx.Client(base_url="http://127.0.0.1:8000", trust_env=False) as client:
        yield client


@pytest.fixture
def make_account():
    url = engine.url
    if url.host not in {"localhost", "127.0.0.1"} or url.database != "lab_agent":
        pytest.fail("账号生命周期测试只允许写入本机 lab_agent 数据库")
    ids = []

    def create(role="student", status=1):
        username = f"pytest_{token_hex(8)}"
        credentials = {"username": username, "password": token_urlsafe(24)}
        with SessionLocal.begin() as db:
            user = User(
                username=username,
                password=hash_password(credentials["password"]),
                name=f"测试-{role}",
                role=role,
                status=status,
                email=f"{username}@example.test",
            )
            db.add(user)
            db.flush()
            user_id = user.id
        ids.append(user_id)
        return user_id, credentials

    try:
        yield create
    finally:
        with SessionLocal.begin() as db:
            db.execute(delete(User).where(User.id.in_(ids)))


def login_headers(api, credentials):
    response = api.post("/api/auth/login", json=credentials)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200, body["message"]
    return {"Authorization": f"Bearer {body['data']['token']}"}


def test_each_token_returns_its_own_profile(api, make_account):
    sessions = []
    for role in ("student", "admin"):
        user_id, credentials = make_account(role=role)
        sessions.append(
            (role, user_id, credentials["username"], login_headers(api, credentials))
        )

    for role, user_id, username, headers in sessions:
        response = api.get("/api/user/info", headers=headers)
        assert response.status_code == 200
        assert response.json() == {
            "code": 200,
            "message": "Ok",
            "data": {
                "id": user_id,
                "username": username,
                "name": f"测试-{role}",
                "role": role,
                "status": 1,
                "email": f"{username}@example.test",
                "phone": None,
            },
        }


@pytest.mark.parametrize(
    ("correct_password", "message"),
    [(True, "The account is banned"), (False, "Wrong account or password")],
)
def test_banned_account_cannot_log_in(api, make_account, correct_password, message):
    _, credentials = make_account(status=0)
    if not correct_password:
        credentials["password"] = "incorrect"
    response = api.post("/api/auth/login", json=credentials)
    assert response.status_code == 200
    assert response.json() == {"code": 500, "message": message, "data": None}


@pytest.mark.parametrize(
    ("change", "message"), [("ban", "用户已被封禁"), ("delete", "用户不存在")]
)
def test_account_change_revokes_access_with_existing_token(
    api, make_account, change, message
):
    user_id, credentials = make_account()
    headers = login_headers(api, credentials)
    before = api.get("/api/user/info", headers=headers)
    assert before.status_code == 200
    assert before.json()["data"]["id"] == user_id

    with SessionLocal.begin() as db:
        if change == "ban":
            db.execute(update(User).where(User.id == user_id).values(status=0))
        else:
            db.execute(delete(User).where(User.id == user_id))

    after = api.get("/api/user/info", headers=headers)
    assert after.status_code == 401
    assert after.json() == {"code": 401, "message": message, "data": None}
