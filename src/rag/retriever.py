

from typing import List
from src.memory.vector_store import VectorMemory


class Retriever:
    def __init__(self, memory: VectorMemory):
        self.memory = memory

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        return self.memory.search(query, k=k)