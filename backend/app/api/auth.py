from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.exception import ServiceException
from app.common.response import Response
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserResponse
from app.utils.jwt import create_access_token
from app.utils.password import verify_password

router = APIRouter(prefix="/auth", tags=["Autherication"])


@router.post("/login")
def auth(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise ServiceException(message="Wrong account or password")

    if user.status != 1:
        raise ServiceException(message="The account is banned")

    token = create_access_token(user.id)

    return Response.success(
        data=LoginResponse(token=token, user=UserResponse.model_validate(user))
    )
