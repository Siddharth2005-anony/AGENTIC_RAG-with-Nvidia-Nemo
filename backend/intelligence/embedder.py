from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()


class Embedder:

    def __init__(self):
        self.embedding_model = NVIDIAEmbeddings(
            model="nvidia/llama-nemotron-embed-1b-v2",
            api_key=os.getenv("NVIDIA_API_KEY")
        )

    def embed_documents(self, texts: list[str]):
        return self.embedding_model.embed_documents(texts)

    def embed_query(self, query: str):
        return self.embedding_model.embed_query(query)