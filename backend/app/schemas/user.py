from enum import IntEnum, StrEnum

from pydantic import BaseModel, ConfigDict


class UserRole(StrEnum):
    STUDENT = "student"
    ADMIN = "admin"


class UserStatus(IntEnum):
    ACTIVE = 1
    BANNED = 0


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    role: UserRole
    phone: str | None = None
    email: str | None = None
    status: UserStatus

    model_config = ConfigDict(from_attributes=True)
