from datetime import datetime, timedelta

import jwt

from app.config import JWT_ALGORITHM, JWT_EXPIRE_HOURS, JWT_SECRET_KEY


def create_access_token(user_id: int) -> str:
    expire = datetime.now() + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
