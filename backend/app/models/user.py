from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = ({"comment": "用户信息表"},)

    username: Mapped[str] = mapped_column(String(50), comment="account", nullable=False)
    password: Mapped[str] = mapped_column(
        String(50), comment="password", nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), comment="nickname", nullable=False)
    role: Mapped[str] = mapped_column(
        String(50), comment="student/admin", nullable=False
    )
    email: Mapped[str | None] = mapped_column(String(50), comment="邮箱")
    phone: Mapped[str | None] = mapped_column(String(50), comment="手机号")
    avatar: Mapped[str | None] = mapped_column(String(50), comment="头像")
    status: Mapped[int] = mapped_column(default=1, comment="0-禁用，1-正常")
