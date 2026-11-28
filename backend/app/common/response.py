from typing import Any

from pydantic import BaseModel


class Response(BaseModel):
    # 统一的封装
    code: int
    message: str
    data: Any = None

    @classmethod
    def success(cls, message: str = "Ok", data: Any = None):
        return cls(code=200, message=message, data=data)

    @classmethod
    def error(cls, code: int = 500, message: str = "Failed"):
        return cls(code=code, message=message)
