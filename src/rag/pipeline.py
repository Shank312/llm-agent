

from src.rag.retriever import Retriever
from src.rag.generator import RAGGenerator


class RAGPipeline:
    def __init__(self, retriever: Retriever, generator: RAGGenerator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str) -> str:
        context = self.retriever.retrieve(query)
        return self.generator.generate(query, context)