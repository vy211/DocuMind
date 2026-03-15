from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schema import Query
from app.rag import ask_question
from app.database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev purposes only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import StreamingResponse

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/ask")
def ask(query: Query):
    return StreamingResponse(ask_question(query.question), media_type="text/plain")
