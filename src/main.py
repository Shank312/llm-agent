

from src.memory.vector_store import VectorMemory
from src.llm.provider import OpenAIProvider

from src.rag.retriever import Retriever
from src.rag.generator import RAGGenerator
from src.rag.pipeline import RAGPipeline
from src.rag.ingest import ingest_documents


# Initialize
memory = VectorMemory()
llm = OpenAIProvider(api_key="YOUR_API_KEY")

# 🔥 Add documents (simulate knowledge base)
documents = [
    "Machine learning is a field of AI that focuses on learning from data.",
    "Neural networks are inspired by the human brain.",
    "Deep learning is a subset of machine learning using neural networks."
]

ingest_documents(memory, documents)

# Build RAG
retriever = Retriever(memory)
generator = RAGGenerator(llm)
rag = RAGPipeline(retriever, generator)

# Run
query = "What is deep learning?"
response = rag.run(query)

print("\n=== RAG RESPONSE ===")
print(response)