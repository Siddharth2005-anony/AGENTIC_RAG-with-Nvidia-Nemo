from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()


class pine_db:

    def __init__(self,index:str):
        self.api_key=os.getenv("PINECONE")

        if not self.api_key:
            raise ValueError("api key not found")

        self.pc = Pinecone(api_key=self.api_key)
        self.index = self.pc.Index(index)

    def upsert(self,data):
        self.index.upsert(vectors=data)
        print("documents pushed succesffully")

    def delete(self,ids):
        self.index.delete(ids=ids)

    def query(self, vector, top_k=5):
        """
        Search similar vectors.
        """
        return self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )

    