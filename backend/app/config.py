import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(verbose=True, dotenv_path=BASE_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_EXPIRE_HOURS: int = int(os.environ["JWT_EXPIRE_HOURS"])
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
