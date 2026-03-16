import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://192.168.0.13:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "tinyllama")


async def get_embedding(text: str) -> list:
    """
    Get a vector embedding for a given text using the Ollama /api/embed endpoint.
    Uses tinyllama by default (since nomic-embed-text may not be installed).
    The /api/embed endpoint returns {"embeddings": [[...]]} (list of lists).
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/embed",
            json={
                "model": EMBED_MODEL,
                "input": text  # /api/embed uses "input", not "prompt"
            }
        )
        response.raise_for_status()
        data = response.json()
        # /api/embed returns {"embeddings": [[0.1, 0.2, ...]]}
        return data["embeddings"][0]
