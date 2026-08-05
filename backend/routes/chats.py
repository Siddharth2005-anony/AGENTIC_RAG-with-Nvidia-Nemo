from fastapi import APIRouter
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


@router.get("/documents/{n}")
def get_docs(n: int):
    return mv_db.query(f"id == {n}")

@router.delete("/del_col")
def del_coll(collection_n1:str):
    return mv_db.delete(collection_n=collection_n1)
