from services.chroma_client import get_chroma_collection
from services.ollama_client import generate_response
from services.embedding_client import get_embedding


async def ask_question(question: str):
    """
    Async generator for the RAG pipeline:
    1. Embed the question.
    2. Search ChromaDB for the most relevant document chunks.
    3. Build a context-aware prompt.
    4. Stream Ollama's response token by token.
    """
    # Try to get relevant context from ChromaDB
    context = ""
    try:
        question_embedding = await get_embedding(question)
        collection = get_chroma_collection()
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3,
            include=["documents", "metadatas"]
        )
        if results["documents"] and results["documents"][0]:
            context_chunks = results["documents"][0]
            sources = [m.get("source", "") for m in results["metadatas"][0]]
            context = "\n\n".join(context_chunks)
            # Add source info
            source_names = list(set(sources))
            context = f"[Source: {', '.join(source_names)}]\n\n{context}"
    except Exception:
        # ChromaDB may not be running — answer from general knowledge
        context = ""

    if context:
        prompt = f"""You are a helpful AI assistant. Answer the question using ONLY the context below.
If the context does not contain enough information to answer, say so honestly.

Context:
{context}

Question: {question}

Answer:"""
    else:
        prompt = f"""You are a helpful AI assistant. Answer the following question:

Question: {question}

Answer:"""

    async for token in generate_response(prompt):
        yield token
