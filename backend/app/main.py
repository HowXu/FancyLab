from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.database import Base, engine

app = FastAPI()
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
