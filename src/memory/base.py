

from typing import List


class BaseMemory:
    def add(self, text: str):
        raise NotImplementedError

    def search(self, query: str, k: int = 3) -> List[str]:
        raise NotImplementedError