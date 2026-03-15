import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

CHROMA_HOST = os.getenv("CHROMA_HOST", "192.168.0.13")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8002"))

def get_chroma_collection(collection_name: str = "documents"):
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return client.get_or_create_collection(collection_name)
