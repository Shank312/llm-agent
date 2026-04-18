

from src.agent.core import LLMAgent
from src.llm.provider import OpenAIProvider
from src.memory.vector_store import VectorMemory
from src.tools.search import SearchTool
from src.tools.calculator import CalculatorTool


llm = OpenAIProvider(api_key="YOUR_KEY")

memory = VectorMemory()

tools = [
    SearchTool(),
    CalculatorTool()
]

agent = LLMAgent(
    llm=llm,
    memory=memory,
    tools=tools
)

print(agent.run("What is machine learning?"))