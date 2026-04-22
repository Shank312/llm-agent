

from src.memory.vector_store import VectorMemory


def ingest_documents(memory: VectorMemory, documents: list[str]):
    for doc in documents:
        memory.add(doc)