import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(verbose=True, dotenv_path=BASE_DIR / '.env')

DATABASE_URL = os.environ["DATABASE_URL"]
