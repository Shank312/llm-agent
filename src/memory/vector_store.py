

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

from src.memory.base import BaseMemory


class VectorMemory(BaseMemory):
    def __init__(self, path: str = "memory.pkl"):
        self.path = path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384

        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts: List[str] = []

        self._load()

    # -------------------------
    # LOAD MEMORY (PERSISTENCE)
    # -------------------------
    def _load(self):
        if not os.path.exists(self.path):
            return

        try:
            with open(self.path, "rb") as f:
                data = pickle.load(f)

                self.index = data.get("index", faiss.IndexFlatL2(self.dimension))
                self.texts = data.get("texts", [])

            print(f"[Memory] Loaded {len(self.texts)} items from disk.")

        except Exception as e:
            print(f"[Memory] Load failed: {e}")

    # -------------------------
    # SAVE MEMORY
    # -------------------------
    def _save(self):
        try:
            with open(self.path, "wb") as f:
                pickle.dump({
                    "index": self.index,
                    "texts": self.texts
                }, f)

        except Exception as e:
            print(f"[Memory] Save failed: {e}")

    # -------------------------
    # ADD MEMORY
    # -------------------------
    def add(self, text: str):
        if not text or not text.strip():
            return

        embedding = self.model.encode([text])[0]

        self.index.add(
            np.array([embedding]).astype("float32")
        )

        self.texts.append(text)

        self._save()

    # -------------------------
    # SEARCH MEMORY
    # -------------------------
    def search(self, query: str, k: int = 3) -> List[str]:
        if len(self.texts) == 0:
            return []

        query_embedding = self.model.encode([query])[0]

        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"),
            min(k, len(self.texts))
        )

        results = []
        for i in I[0]:
            if i < len(self.texts):
                results.append(self.texts[i])

        return results