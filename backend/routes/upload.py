from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from clerks.validator import validate_file
from clerks.loader import load_document
from clerks.cleaner import clean_text
from clerks.splitter import split_document
from clerks.metadata import generate_metadata

from intelligence.embedder import Embedder
from database.milvus_client import milvus_clerk


router = APIRouter()


UPLOAD_FOLDER = Path("storage/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # -----------------------------
    # validate
    # -----------------------------
    validate_file(file)

    # -----------------------------
    # save
    # -----------------------------
    extension = Path(file.filename).suffix

    unique_name = f"{uuid.uuid4()}{extension}"

    saved_path = UPLOAD_FOLDER / unique_name

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # load text
    # -----------------------------
    raw_text = load_document(saved_path)

    # -----------------------------
    # clean
    # -----------------------------
    cleaned_text = clean_text(raw_text)

    # -----------------------------
    # split
    # -----------------------------
    chunks = split_document(cleaned_text)

    # -----------------------------
    # embeddings
    # -----------------------------
    embedder = Embedder()

    vectors = embedder.embed_documents(chunks)

    # -----------------------------
    # metadata
    # -----------------------------
    metadata = generate_metadata(
        chunks=chunks,
        filename=file.filename
    )

    # -----------------------------
    # database
    # -----------------------------
    db = milvus_clerk(
        db_name="demo.db",
        collection_name="documents",
        dimension=2048
    )

    db.insert(
        vectors=vectors,
        texts=chunks,
        metadata=metadata
    )

    return {
        "status": "success",
        "filename": file.filename,
        "chunks": len(chunks)
    }
