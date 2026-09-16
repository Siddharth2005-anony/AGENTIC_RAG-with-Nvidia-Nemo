from pymilvus import MilvusClient
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import os

embedding_model = NVIDIAEmbeddings(
    model="nvidia/Nemotron-3-Embed-1B-BF16",
    api_key=os.getenv("NVIDIA_API_KEY")
)


def embed_query(text: str) -> list[float]:
    return embedding_model.embed_query(text)


def search_milvus(question: str) -> dict:
    """
    Search company documents using Milvus.

    Use this tool for:
    - Company policies
    - Reports
    - General knowledge
    - Document-based questions

    Args:
        question: User's question.

    Returns:
        Relevant document chunks.
    """

    try:
        client = MilvusClient(
            uri=os.getenv("MILVUS_URI"),
            token=os.getenv("MILVUS_TOKEN") or None
        )

        query_vector = embed_query(question)

        results = client.search(
            collection_name=os.getenv("MILVUS_COLLECTION"),
            data=[query_vector],
            limit=5,
            output_fields=["text"]
        )

        documents = []

        for result in results[0]:

            entity = result.get("entity", {})

            documents.append({
                "text": entity.get("text", ""),
                "distance": result.get("distance")
            })

        return {
            "status": "success",
            "documents": documents
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }