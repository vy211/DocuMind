import io
import uuid
from pypdf import PdfReader
from services.embedding_client import get_embedding
from services.chroma_client import get_chroma_collection


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file given its raw bytes."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split raw text into overlapping chunks.
    Overlap ensures context isn't lost at chunk boundaries.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c for c in chunks if c.strip()]  # Filter empty/whitespace chunks


async def process_and_store_pdf(filename: str, file_bytes: bytes) -> dict:
    """
    Full pipeline:
    1. Extract text from PDF
    2. Chunk it
    3. Embed each chunk via Ollama
    4. Store in ChromaDB
    Returns a summary with chunk count and doc_id.
    """
    # 1. Extract text
    raw_text = extract_text_from_pdf(file_bytes)
    if not raw_text:
        raise ValueError("Could not extract any text from the PDF. Is it a scanned image?")

    # 2. Chunk the text
    chunks = chunk_text(raw_text)

    # 3. Embed each chunk and prepare for ChromaDB
    doc_id = str(uuid.uuid4())
    embeddings = []
    documents = []
    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        embedding = await get_embedding(chunk)
        embeddings.append(embedding)
        documents.append(chunk)
        ids.append(f"{doc_id}_chunk_{i}")
        metadatas.append({"source": filename, "doc_id": doc_id, "chunk_index": i})

    # 4. Store in ChromaDB
    collection = get_chroma_collection()
    collection.upsert(
        embeddings=embeddings,
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    return {
        "doc_id": doc_id,
        "filename": filename,
        "chunk_count": len(chunks),
        "character_count": len(raw_text)
    }
