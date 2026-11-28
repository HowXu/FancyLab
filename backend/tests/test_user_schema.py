import pytest
from pydantic import ValidationError

from app.schemas.user import UserResponse, UserRole, UserStatus


def test_user_response():
    user = UserResponse.model_validate(
        {"id": 1, "username": "s1", "name": "张三", "role": "student", "status": 1}
    )

    assert user.role is UserRole.STUDENT
    assert user.status is UserStatus.ACTIVE

    data = user.model_dump(mode="json")
    assert data["role"] == "student"
    assert data["status"] == 1


@pytest.mark.parametrize(
    ("role", "status", "invalid_field"),
    [("unknown", 1, "role"), ("student", 99, "status")],
)
def test_user_response_reject(role, status, invalid_field):
    with pytest.raises(ValidationError) as e:
        UserResponse.model_validate(
            {"id": 1, "username": "s1", "name": "张三", "role": role, "status": status}
        )
    assert e.value.errors()[0]["loc"] == (invalid_field,)
