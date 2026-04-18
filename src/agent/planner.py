

class Planner:
    def __init__(self, llm):
        self.llm = llm

    def plan(self, state):
        prompt = f"""
You are an AI agent.

User query: {state.query}

Previous steps:
{state.steps}

Decide next action:
- search
- calculate
- finish

Return JSON:
{{"type": "...", "input": "..."}}
"""

        response = self.llm.generate(prompt)

        # TODO: parse JSON safely
        return eval(response)