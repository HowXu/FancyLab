from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.response import Response


class ServiceException(Exception):
    # 服务异常类型
    def __init__(self, message: str, code: int = 500) -> None:
        self.message = message
        self.code = code
        super().__init__(message)


async def service_exception_handler(request: Request, e: Exception):

    if not isinstance(e, ServiceException):
        raise e

    return JSONResponse(
        status_code=200,
        content=Response.error(code=e.code, message=e.message).model_dump(),
    )


async def http_exception_handler(request: Request, e: Exception):

    if not isinstance(e, HTTPException):
        raise e

    return JSONResponse(
        status_code=e.status_code,
        content=Response.error(code=e.status_code, message=e.detail).model_dump(),
    )


async def validation_exception_handler(request: Request, e: Exception):

    if not isinstance(e, RequestValidationError):
        raise e

    return JSONResponse(
        status_code=422,
        content=Response.error(
            code=422, message="Valiadte request paraments"
        ).model_dump(),
    )


async def global_exception_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=500,
        content=Response.error(code=500, message="Internal Server Error").model_dump(),
    )
