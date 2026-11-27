from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.jwt_auth import get_current_user

router = APIRouter(prefix="/user", tags=["用户接口"])


@router.get("/info")
def get_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "code": 200,
        "message": "Ok",
        "data": UserResponse.model_validate(current_user),
    }
