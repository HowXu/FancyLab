import asyncio
import json
from http import HTTPStatus

from fastapi import Request

from app.common.exception import global_exception_handler


def test_global_exception_returns_generic_error():
    request = Request({"type": "http", "method": "GET", "path": "/"})
    response = asyncio.run(
        global_exception_handler(request, RuntimeError("internal detail"))
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert json.loads(bytes(response.body)) == {
        "code": 500,
        "message": "Internal Server Error",
        "data": None,
    }
