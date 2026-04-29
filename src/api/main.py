

from fastapi import FastAPI
from src.api.routes import chat, rag, memory, logs

app = FastAPI(title="LLM Agent API", version = "1,0")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
app.include_router(memory.router, prefix="/memory", tags=["Memory"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])



@app.get("/")
def root():
    return{"message": "LLM Agent API running"}