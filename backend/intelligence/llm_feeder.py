import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMBaby:

    def __init__(self, api_key: str = None):
        # Uses passed api_key first, otherwise checks environment variables
        key = api_key or os.getenv("OPENAI")
        if key:
            key = key.strip()
        self.client = OpenAI(api_key=key)

    def swallow(self, results: list, query: str) -> str:
        system_m = (
            "You are a helpful RAG assistant.\n"
            "Answer using ONLY the provided context.\n"
            "If the context does not contain enough information to answer the query, "
            "politely state that you do not know.\n"
            "Do not rely on prior knowledge or make assumptions."
        )

        # Formatted clearly without broken quote blocks
        user_content = f"### Context:\n{results}\n\n### Query:\n{query}"

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_m},
                {"role": "user", "content": user_content},
            ],
        )

        return response.choices[0].message.content



