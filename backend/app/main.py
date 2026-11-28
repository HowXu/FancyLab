from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api import router as api_router
from app.common.exception import (
    ServiceException,
    global_exception_handler,
    http_exception_handler,
    service_exception_handler,
    validation_exception_handler,
)
from app.database import Base, engine

app = FastAPI()
app.include_router(api_router)
Base.metadata.create_all(bind=engine)

app.add_exception_handler(ServiceException, service_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
