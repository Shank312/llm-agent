

from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    query: str


class MemoryRequest(BaseModel):
    text: str


class RAGRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str