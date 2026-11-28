from io import BytesIO

import pytest
from fastapi import UploadFile

from app.api import files
from app.common.exception import ServiceException


@pytest.fixture(autouse=True)
def upload_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(files, "UPLOAD_DIR", tmp_path)


def upload(name: str, content: bytes):
    with BytesIO(content) as stream:
        return files.upload(UploadFile(stream, filename=name, size=len(content)))


def test_upload_saves_file_and_returns_metadata(tmp_path):
    content = b"sample document"
    response = upload("Report.PDF", content)

    assert response.code == 200
    data = response.data
    disk_name = data["disk_name"]
    assert disk_name.endswith(".pdf")
    assert data == {
        "original_name": "Report.PDF",
        "disk_name": disk_name,
        "size": len(content),
        "url": f"/uploads/{disk_name}",
    }
    assert (tmp_path / disk_name).read_bytes() == content


def test_upload_same_name_keeps_both_files(tmp_path):
    first = upload("notes.pdf", b"first").data["disk_name"]
    second = upload("notes.pdf", b"second").data["disk_name"]

    assert first != second
    assert (tmp_path / first).read_bytes() == b"first"
    assert (tmp_path / second).read_bytes() == b"second"


@pytest.mark.parametrize(
    ("name", "message"),
    [
        ("", "文件名不能为空"),
        ("report.txt", "不支持的文件后缀: .txt"),
        ("report", "不支持的文件后缀: "),
    ],
)
def test_upload_rejects_invalid_names_without_writing(name, message, tmp_path):
    with pytest.raises(ServiceException) as exc:
        upload(name, b"hello")

    assert exc.value.message == message
    assert not list(tmp_path.iterdir())


def test_upload_enforces_inclusive_size_limit(monkeypatch, tmp_path):
    monkeypatch.setattr(files, "MAX_FILE_SIZE", 4)
    saved = upload("limit.pdf", b"1234").data["disk_name"]

    with pytest.raises(ServiceException, match="文件大小不能超过"):
        upload("over.pdf", b"12345")

    assert list(tmp_path.iterdir()) == [tmp_path / saved]
    assert (tmp_path / saved).read_bytes() == b"1234"
