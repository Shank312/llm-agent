

from typing import List, Dict, Any
from dataclasses import dataclass

from src.agent.executor import ToolExecutor
from src.agent.planner import Planner
from src.memory.base import BaseMemory
from src.llm.provider import LLMProvider


@dataclass
class AgentState:
    query: str
    steps: List[Dict[str, Any]]
    final_answer: str = ""


class LLMAgent:
    def __init__(
        self,
        llm: LLMProvider,
        memory: BaseMemory,
        tools: List[Any],
        max_steps: int = 5,
    ):
        self.llm = llm
        self.memory = memory
        self.executor = ToolExecutor(tools)
        self.planner = Planner(llm)
        self.max_steps = max_steps

    def run(self, query: str) -> str:
        # 🔥 STEP 1: Retrieve relevant past memory
        try:
            past_context = self.memory.search(query)
        except Exception:
            past_context = []

        # Combine query with retrieved memory context
        enriched_query = query
        if past_context:
            enriched_query += "\n\nRelevant memory:\n" + "\n".join(past_context)

        state = AgentState(
            query=enriched_query,
            steps=[]
        )

        # 🔁 STEP 2: Iterative planning + execution loop
        for step in range(self.max_steps):
            action = self.planner.plan(state)

            if action["type"] == "finish":
                state.final_answer = action.get("output", "")
                break

            result = self.executor.execute(action)

            state.steps.append({
                "action": action,
                "result": result
            })

        # 🧠 STEP 3: Store interaction in memory
        try:
            if state.final_answer:
                memory_entry = f"Q: {query}\nA: {state.final_answer}"
                self.memory.add(memory_entry)
        except Exception:
            pass  # Avoid breaking main flow due to memory issues

        return state.final_answer