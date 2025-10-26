

LLM Agent (MVP) — README 

Files:
  src/agent.py       - LangChain agent wrapper and logging
  src/tools.py       - search_tool and exec_tool implementations
  src/run_agent.py   - CLI entrypoint: `python -m src.run_agent --prompt "..."`

Setup (suggested):
  1) Create virtualenv: python -m venv venv && source venv/bin/activate
  2) Install dependencies:
       pip install langchain openai requests pytest
     (If you want a different LLM, configure LANGCHAIN settings or pass a different llm to build_agent)

Usage:
  # run from project root (llm-agent/)
  python -m src.run_agent --prompt "Search Python decorators and show a minimal example"

  # raw JSON
  python -m src.run_agent --prompt "print something" --raw

Logs:
  JSONL logs written to logs/agent_logs.jsonl

Safety & sandboxing notes:
  - exec_tool runs Python in a subprocess with CPU and memory limits where supported (Unix 'resource' module).
    This is a lightweight sandbox intended for development and tests — it is NOT perfect isolation.
    For production, use OS containers, firejail, chroot, or a dedicated sandboxing service.
  - search_tool uses DuckDuckGo Instant Answer API (no API key). Network failures yield a placeholder response.
  - The LangChain agent will call these tools by name; tools return JSON-serializable strings.

Unit tests:
  pytest -q

Windows notes:
  - The `resource` module is not available on Windows. In that case `exec_tool` will still run but CPU/memory limits won't be enforced via `resource`.
