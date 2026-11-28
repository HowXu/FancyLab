import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 100 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".zip",
}


load_dotenv(verbose=True, dotenv_path=BASE_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_EXPIRE_HOURS: int = int(os.environ["JWT_EXPIRE_HOURS"])
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
