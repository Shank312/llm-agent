🧠 LLM Agent Framework (Production-Ready)

  A modular, extensible AI agent system for building autonomous workflows using LLMs, tools, and memory.


🚀 Overview

This project implements a production-style AI agent architecture that simulates how real-world intelligent systems operate.

Unlike basic LLM wrappers, this system includes:

  🧠 Reasoning loop (planner + executor)
  🛠 Tool usage (search, calculator, file ops)
  💾 Persistent memory (vector database)
  🔌 Modular architecture for extensibility

👉 Designed to reflect industry-grade AI system design


🎯 Key Features
   ✅ Multi-step reasoning agent loop
   ✅ Tool execution system (search, calculator, etc.)
   ✅ Long-term memory using vector embeddings (FAISS)
   ✅ Modular architecture (agent, tools, memory, LLM abstraction)
   ✅ Configurable workflows
   ✅ Structured logging system


 🏗️ Architecture
 
 User Query
   ↓
Memory Retrieval (Vector DB)
   ↓
Planner (LLM decides next action)
   ↓
Executor (runs tools)
   ↓
Memory Storage (persist knowledge)
   ↓
Final Response


📂 Project Structure

llm-agent/
│
├── src/
│   ├── agent/
│   │   ├── core.py          # Agent loop
│   │   ├── planner.py       # Decision making
│   │   ├── executor.py      # Tool execution
│   │
│   ├── memory/
│   │   ├── base.py
│   │   ├── vector_store.py  # FAISS memory
│   │
│   ├── tools/
│   │   ├── search.py
│   │   ├── calculator.py
│   │
│   ├── llm/
│   │   ├── provider.py      # LLM abstraction
│   │
│   ├── utils/
│   │   ├── logger.py
│   │
│   └── main.py
│
├── logs/
├── tests/
├── README.md
├── requirements.txt


⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/Shank312/llm-agent.git
cd llm-agent

2️⃣ Create virtual environment
python -m venv venv

Activate:
Windows:
venv\Scripts\activate

Linux/macOS:
source venv/bin/activate

3️⃣ Install dependencies:
pip install -r requirements.txt

▶️ Running the Agent:
python src/main.py

🧪 Example Usage:
from src.agent.core import LLMAgent
from src.memory.vector_store import VectorMemory
from src.llm.provider import OpenAIProvider

memory = VectorMemory()

agent = LLMAgent(
    llm=OpenAIProvider(api_key="YOUR_API_KEY"),
    memory=memory,
    tools=[]
)

response = agent.run("Explain machine learning simply")
print(response)


🧠 Memory System

This agent includes a persistent memory layer:

🔹 Short-Term Memory
Maintains current session context
🔹 Long-Term Memory
   Uses FAISS vector database
   Stores past queries and responses
   Retrieves relevant context dynamically

👉 Enables context-aware and evolving AI behavior


🛠️ Tools System

The agent supports extensible tools:
| Tool          | Description            |
| ------------- | ---------------------- |
| 🔍 Search     | Web search integration |
| 🧮 Calculator | Math operations        |
| 📂 FileReader | Read files             |


🔌 LLM Support

Abstracted LLM layer allows easy switching:

OpenAI (GPT)
Anthropic (Claude)
Local models (Ollama, Llama)


📊 Capabilities:
Multi-step reasoning
Tool-based problem solving
Context-aware responses
Memory-augmented intelligence
Extensible agent workflows


🗺️ Roadmap:
 RAG pipeline (documents, PDFs)
 Async execution (high scalability)
 Streaming responses
 LangGraph integration
 Web dashboard for logs
 Docker deployment


 ⚠️ Limitations:
Planner uses simple prompt-based reasoning (can be improved)
No streaming support yet
Limited tool ecosystem (extensible)


🤝 Contributing

Contributions are welcome!

git checkout -b feature-name
git commit -m "Add feature"
git push origin feature-name


📜 License

MIT License


👨‍💻 Author

Shankar Kumar
AI Engineer | Backend Developer
