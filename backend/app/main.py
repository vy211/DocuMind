from fastapi import FastAPI
from models.schema import Query
from app.rag import ask_question
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/ask")
def ask(query: Query):
    answer = ask_question(query.question)
    return {"answer": answer}
