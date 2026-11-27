from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.schemas.user import UserResponse
from app.utils.jwt import create_access_token
from app.utils.password import verify_password

router = APIRouter(prefix="/auth", tags=["Autherication"])


@router.post("/login")
def auth(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        return {"code": 400, "message": "Error username or password"}

    if user.status != 1:
        return {"code": 403, "message": "The account is been banned"}

    token = create_access_token(user.id)

    return {
        "code": 200,
        "message": "Ok",
        "data": {"token": token, "user": UserResponse.model_validate(user)},
    }
