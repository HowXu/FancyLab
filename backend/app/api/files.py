import shutil
import time
import uuid
from os import path

from fastapi import APIRouter, UploadFile

from app.common.exception import ServiceException
from app.common.response import Response
from app.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR

router = APIRouter(prefix="/files", tags=["文件管理"])


def upload(file: UploadFile):
    if not file.filename:
        raise ServiceException("文件名不能为空")

    original_name = path.basename(file.filename)
    extension = path.splitext(original_name)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ServiceException(f"不支持的文件后缀: {extension}")

    if file.size and file.size > MAX_FILE_SIZE:
        raise ServiceException(f"文件大小不能超过 {MAX_FILE_SIZE // 1024 // 1024} MiB")

    disk_name = f"{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}{extension}"
    save_path = UPLOAD_DIR / disk_name

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return Response.success(
        data={
            "original_name": original_name,
            "disk_name": disk_name,
            "size": file.size,
            "url": f"/uploads/{disk_name}",
        }
    )
