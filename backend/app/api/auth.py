from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import Response
from app.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autherication"])


@router.post("/login")
def auth(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    result = auth_service.login(db, data)
    return Response.success(message="Login Success", data=result)


@router.post("/register")
def register(data: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    auth_service.register(db, data)
    return Response.success(message="Register Success")
