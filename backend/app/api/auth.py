from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api/auth", tags=["Autherication"])


@router.post("/login")
def auth(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or user.password != data.password:
        return {"code": 400, "message": "Error username or password"}
    return {"code": 200, "message": "Done", "data": UserResponse.model_validate(user)}
