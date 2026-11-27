from fastapi import FastAPI

from app.api import router as api_router
from app.database import Base, engine

app = FastAPI()
app.include_router(api_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
