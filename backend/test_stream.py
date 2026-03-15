import requests
import time
import argparse
import os
from dotenv import load_dotenv

# Load environment variables, primarily to get the home server IP for Ollama
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://192.168.0.13:11434/api/generate")
FASTAPI_URL = "http://localhost:8000/ask"

def test_ollama_direct(prompt: str, model: str = "tinyllama"):
    """Tests the direct connection to the bare Ollama server."""
    print(f"=== Testing Direct Ollama Stream ===")
    print(f"Target: {OLLAMA_URL}")
    print(f"Model : {model}")
    print(f"Prompt: '{prompt}'\n")
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            },
            stream=True,
            timeout=10 # In case the server is down
        )
        response.raise_for_status()
        
        start_time = time.time()
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                # Decode and print individual chunks as they come over the wire
                print(f"[+{time.time() - start_time:.3f}s] {chunk.decode()}", flush=True, end="")
                
        print(f"\n\n=== Direct Ollama Stream Complete ({time.time() - start_time:.2f}s) ===\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Ollama directly. Error: {e}\n")


def test_fastapi_backend(prompt: str):
    """Tests the FastAPI backend's streaming capabilities."""
    print(f"=== Testing FastAPI Backend Stream ===")
    print(f"Target: {FASTAPI_URL}")
    print(f"Prompt: '{prompt}'\n")
    
    try:
        response = requests.post(
            FASTAPI_URL,
            json={"question": prompt},
            stream=True,
            timeout=10
        )
        response.raise_for_status()
        
        start_time = time.time()
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                # The backend just sends text, not JSON
                print(f"[+{time.time() - start_time:.3f}s] {chunk.decode()}", flush=True, end="")
                
        print(f"\n\n=== FastAPI Stream Complete ({time.time() - start_time:.2f}s) ===\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to FastAPI backend. Error: {e}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Streaming Endpoints for DocuMind.")
    parser.add_argument("--test", choices=["all", "ollama", "api"], default="all", help="Which endpoint to test.")
    parser.add_argument("--prompt", type=str, default="Write a short, tiny poem about a cat.", help="The question/prompt to ask.")
    
    args = parser.parse_args()
    
    if args.test in ["all", "ollama"]:
        test_ollama_direct(args.prompt)
        time.sleep(1) # Slight delay between tests
        
    if args.test in ["all", "api"]:
        test_fastapi_backend(args.prompt)
