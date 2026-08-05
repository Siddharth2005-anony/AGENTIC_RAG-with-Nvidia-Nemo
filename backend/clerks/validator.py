from pathlib import Path
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx"
}

MAX_FILE_SIZE = 20 * 1024 * 1024   # 20 MB


def validate_file(file: UploadFile):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File exceeds maximum size."
        )

    return True