from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "qwen3:8b"
    )

    REDIS_HOST = os.getenv(
        "REDIS_HOST",
        "localhost"
    )

    REDIS_PORT = int(
        os.getenv("REDIS_PORT", 6379)
    )

    REDIS_PASSWORD = os.getenv(
        "REDIS_PASSWORD", ""
    )

    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv("PORT", 8000)
    )

    TOP_K = int(
        os.getenv("TOP_K", 5)
    )


settings = Settings()