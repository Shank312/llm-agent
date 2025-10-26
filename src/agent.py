

python - <<'PY'
from pathlib import Path
p = Path("src/agent.py")
p.write_text(r'''# src/agent.py
"""
Unified agent wrapper supporting LangChain v1 (create_agent) and older langchain APIs.
"""
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

from .tools import search_tool, exec_tool

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "agent_logs.jsonl"))
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

class JSONLineLogger(logging.Handler):
    def __init__(self, path: str):
        super().__init__()
        self.path = path
    def emit(self, record):
        try:
            payload = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "message": record.getMessage(),
                **(record.__dict__.get("extra", {}) or {})
            }
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload, default=str) + "\\n")
        except Exception:
            pass

logger = logging.getLogger("llm_agent")
logger.setLevel(logging.INFO)
logger.addHandler(JSONLineLogger(LOG_PATH))

def _log_event(name: str, data: Dict[str, Any]):
    logger.info(name, extra={"extra": data})

def build_agent(llm: Optional[Any] = None) -> Optional[Any]:
    # Try LangChain v1 API first
    try:
        from langchain.agents import create_agent  # type: ignore
        from langchain.tools import tool  # type: ignore
        try:
            from langchain.chat_models import ChatOpenAI  # type: ignore
        except Exception:
            ChatOpenAI = None  # type: ignore

        @tool
        def web_search_tool(query: str) -> str:
            return json.dumps(search_tool(query))

        @tool
        def exec_python_tool(code: str) -> str:
            return json.dumps(exec_tool(code))

        if llm is None and ChatOpenAI is not None:
            try:
                llm = ChatOpenAI(temperature=0)
            except Exception:
                llm = None

        agent = create_agent(llm=llm, tools=[web_search_tool, exec_python_tool])
        return agent
    except Exception as e_v1:
        _log_event("build_agent.langchain_v1_failed", {"error": str(e_v1)})

    # Try older LangChain API
    try:
        from langchain.agents import Tool, initialize_agent, AgentType  # type: ignore
        try:
            from langchain.chat_models import ChatOpenAI  # type: ignore
        except Exception:
            ChatOpenAI = None  # type: ignore

        if llm is None and ChatOpenAI is not None:
            try:
                llm = ChatOpenAI(temperature=0)
            except Exception:
                llm = None

        tools = [
            Tool(name="web_search", func=lambda q: json.dumps(search_tool(q)),
                 description="Search the web or docs. Input: query string. Output: JSON string."),
            Tool(name="exec_python", func=lambda code: json.dumps(exec_tool(code)),
                 description="Execute python code. Input: code string. Output: JSON string."),
        ]
        agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
        return agent
    except Exception as e_old:
        _log_event("build_agent.langchain_old_failed", {"error": str(e_old)})

    return None

def run_prompt(prompt: str, llm: Optional[Any] = None, return_raw: bool = False) -> Dict[str, Any]:
    _log_event("agent_run.start", {"prompt": prompt})
    agent = build_agent(llm=llm)
    if agent is None:
        msg = "LangChain agent could not be initialized in this environment (incompatible or missing langchain/LLM)."
        entry = {"prompt": prompt, "response": msg, "timestamp": datetime.utcnow().isoformat() + "Z", "fallback": True}
        _log_event("agent_run.fallback", entry)
        if return_raw:
            return entry
        return {"prompt": prompt, "response": msg, "ok": True, "fallback": True}
    try:
        res = agent.run(prompt)
        entry = {"prompt": prompt, "response": res, "timestamp": datetime.utcnow().isoformat() + "Z"}
        _log_event("agent_run.complete", entry)
        if return_raw:
            return entry
        return {"prompt": prompt, "response": res, "ok": True}
    except Exception as e:
        _log_event("agent_run.error", {"prompt": prompt, "error": str(e)})
        return {"prompt": prompt, "response": None, "ok": False, "error": str(e)}
''', encoding='utf-8')
print("WROTE src/agent.py")
PY
