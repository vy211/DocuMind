import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://192.168.0.13:11434/api/generate")

async def generate_response(prompt: str, model: str = "tinyllama"):
    """
    Async generator that streams tokens from Ollama one at a time.
    Uses httpx instead of requests so it works correctly with FastAPI's async event loop.
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            yield chunk["response"]
                    except json.JSONDecodeError:
                        continue
