from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models.schema import Query
from app.rag import ask_question
from app.database import init_db
from app.upload import process_and_store_pdf
from services.chroma_client import get_chroma_collection

app = FastAPI(title="DocuMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def health():
    return {"status": "DocuMind backend is running"}


@app.post("/ask")
async def ask(query: Query):
    """Stream an AI response to a question, using uploaded docs as context."""
    return StreamingResponse(ask_question(query.question), media_type="text/plain")


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, extract its text, embed it, and store in ChromaDB."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        result = await process_and_store_pdf(file.filename, file_bytes)
        return {
            "success": True,
            "message": f"Successfully processed '{file.filename}' into {result['chunk_count']} chunks.",
            **result
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


@app.get("/documents")
def list_documents():
    """List all unique documents stored in ChromaDB."""
    try:
        collection = get_chroma_collection()
        results = collection.get(include=["metadatas"])
        
        # Deduplicate by filename
        seen = {}
        for meta in results.get("metadatas", []):
            fname = meta.get("source", "unknown")
            doc_id = meta.get("doc_id", "")
            if fname not in seen:
                seen[fname] = doc_id
        
        return {
            "documents": [{"filename": k, "doc_id": v} for k, v in seen.items()]
        }
    except Exception:
        return {"documents": []}
