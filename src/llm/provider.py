

# src/llm/provider.py

from abc import ABC, abstractmethod
from typing import Optional
from openai import OpenAI


class LLMProvider(ABC):
    """
    Base abstraction for all LLM providers.
    """

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the LLM.
        """
        pass


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of LLMProvider.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response using OpenAI Chat Completions API.
        """

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response.choices[0].message.content.strip()