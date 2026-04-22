

class RAGGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, query: str, context: list[str]) -> str:
        context_text = "\n".join(context)

        prompt = f"""
You are a helpful AI assistant.

Use the following context to answer the question.

Context:
{context_text}

Question:
{query}

Answer clearly and concisely.
"""

        return self.llm.generate(prompt)