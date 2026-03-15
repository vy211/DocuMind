from services.chroma_client import get_chroma_collection
from services.ollama_client import generate_response

def ask_question(question: str) -> str:
    collection = get_chroma_collection()
    
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    if not results["documents"] or not results["documents"][0]:
        context = ""
    else:
        context = " ".join(results["documents"][0])

    prompt = f"""
Answer the question using the context.

Context:
{context}

Question:
{question}
"""

    return generate_response(prompt)
