from sqlalchemy.orm import Session

from app.common.exception import ServiceException
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.user import UserResponse, UserRole, UserStatus
from app.utils.jwt import create_access_token
from app.utils.password import hash_password, verify_password


def login(db: Session, data: LoginRequest):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise ServiceException(message="Wrong account or password")

    if user.status != 1:
        raise ServiceException(message="The account is banned")

    token = create_access_token(user.id)
    return LoginResponse(token=token, user=UserResponse.model_validate(user))


def register(db: Session, data: RegisterRequest):
    user = db.query(User).filter(User.username == data.username).first()

    if user:
        raise ServiceException(message="This account has been registered!")

    user = User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name or data.username,
        role=UserRole.STUDENT,
        status=UserStatus.ACTIVE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
