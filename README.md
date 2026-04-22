# 🧠 LLM Agent Framework (Production-Ready)

🚀 **Built by a Full Stack AI Engineer**

A modular, production-style AI agent system with:

- 🔁 Multi-step reasoning (Planner + Executor)
- 🧰 Tool execution system
- 🧠 Long-term memory (FAISS vector DB)
- 📚 Retrieval-Augmented Generation (RAG)
- ⚙️ Extensible architecture for real-world AI systems

---

## 🚀 Overview

This project simulates how **real-world AI systems (like ChatGPT, Copilot, AutoGPT)** are designed internally.

It is **not just an LLM wrapper**, but a complete system with:

- Planning
- Tool usage
- Memory
- Knowledge retrieval (RAG)

💡 Built with a **full-stack AI engineering mindset** — backend architecture + intelligent systems design.

---

## 🏗 System Architecture

User Query
↓
Memory Retrieval (Vector DB)
↓
Planner (LLM decides next step)
↓
Executor (Tools / RAG / Logic)
↓
Memory Storage
↓
Final Response


---

## 📚 RAG Pipeline (Major Upgrade 🚀)

This project now includes a **complete RAG system**:

### Components

- 🔍 **Retriever** → Fetches relevant knowledge
- 🧠 **Generator** → LLM generates contextual answer
- 🔗 **Pipeline** → Connects retrieval + generation
- 📥 **Ingestion** → Adds documents to vector memory

### Example

```python
from src.memory.vector_store import VectorMemory
from src.llm.provider import OpenAIProvider

from src.rag.retriever import Retriever
from src.rag.generator import RAGGenerator
from src.rag.pipeline import RAGPipeline
from src.rag.ingest import ingest_documents

memory = VectorMemory()
llm = OpenAIProvider(api_key="YOUR_API_KEY")

documents = [
    "Machine learning learns from data.",
    "Deep learning uses neural networks."
]

ingest_documents(memory, documents)

rag = RAGPipeline(
    retriever=Retriever(memory),
    generator=RAGGenerator(llm)
)

response = rag.run("What is deep learning?")
print(response)

🧠 Memory System
🔹 Short-term → current session context
🔹 Long-term → FAISS vector database
🔹 Stores past queries + responses
🔹 Enables context-aware reasoning

🧰 Tools System
| Tool          | Description            |
| ------------- | ---------------------- |
| 🔍 Search     | Web search integration |
| 🧮 Calculator | Math operations        |
| 📂 FileReader | Read files             |

🔌 LLM Layer (Abstracted)

Supports multiple providers:

OpenAI (GPT)
Anthropic (Claude)
Local models (Ollama / LLaMA)

👉 Easily switch models without changing core logic


📂 Project Structure
llm-agent/
│── src/
│   ├── agent/
│   │   ├── core.py        # Agent loop
│   │   ├── planner.py     # Decision logic
│   │   ├── executor.py    # Tool execution
│
│   ├── memory/
│   │   ├── base.py
│   │   ├── vector_store.py   # FAISS
│
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   ├── pipeline.py
│   │   ├── ingest.py
│
│   ├── llm/
│   │   ├── provider.py
│
│   ├── tools.py
│   ├── main.py
│   ├── run_agent.py
│
│── tests/
│── logs/
│── README.md


⚙️ Installation
git clone https://github.com/Shank312/llm-agent.git
cd llm-agent

python -m venv venv


Activate

Windows:
venv\Scripts\activate

Linux/macOS:
source venv/bin/activate

Install
pip install -r requirements.txt

▶️ Run
python src/main.py


⚡ Capabilities
Multi-step reasoning agent
Tool-based execution
Memory-augmented intelligence
Retrieval-augmented generation (RAG)
Modular and extensible architecture


🛣 Roadmap
 PDF ingestion (real documents)
 Async agent execution
 Streaming responses
 FastAPI backend (API layer)
 Web dashboard (logs + memory visualization)
 Docker deployment


⚠️ Limitations
Planner uses prompt-based reasoning (can be improved)
No streaming support yet
Tool ecosystem is minimal (extensible)


🤝 Contributing:
git checkout -b feature-name
git commit -m "feat: add feature"
git push origin feature-name


📄 License

MIT License


👨‍💻 Author

Shankar Kumar
🚀 Full Stack AI Engineer
💻 Backend Systems | 🤖 AI/ML | ⚙️ Scalable Architectures
