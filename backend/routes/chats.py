from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from intelligence.embedder import Embedder
from intelligence.llm_feeder import LLMBaby
from database.milvus_client import milvus_clerk

router = APIRouter()

engine = Embedder()

mv_db = milvus_clerk(
    db_name="demo.db",
    collection_name="documents",
    dimension=1024
)

baby = LLMBaby()


class Queryrequest(BaseModel):
    query: str


@router.post("/NVIDIA")
def embedding(user_query: Queryrequest):

    vc_query = engine.embed_query(user_query.query)

    data = mv_db.search(vc_query)

    results = [
        (item["distance"], item["entity"]["text"])
        for item in data[0]
    ]

    final_response = baby.swallow(
        results=results,
        query=user_query.query
    )

    return {
        "answer": final_response
    }


@router.get("/collections")
def get_collections():
    return mv_db.list()


@router.delete("/collections/{collection_name}")
def delete_collection(
    collection_name: str = Path(..., min_length=1, max_length=255),
):
    """Delete one available Milvus collection by name."""
    try:
        result = mv_db.delete(collection_n=collection_name)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The collection could not be deleted.",
        ) from exc

    if result["msg"] == "collection does not exist":
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' was not found.",
        )

    return {
        "status": "success",
        "collection": collection_name,
        "message": "Collection deleted successfully.",
    }


@router.get("/documents/{n}")
def get_docs(n: int):
    return mv_db.query(f"id == {n}")

@router.delete("/del_col")
def del_coll(collection_n1:str):
    """Keep the original endpoint available for existing clients."""
    return mv_db.delete(collection_n=collection_n1)
