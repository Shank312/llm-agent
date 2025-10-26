# tests/test_tools.py
# Ensure repo root is on sys.path so `import src` works under pytest.
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import json
import os
import sys
import time

from src.tools import exec_tool, search_tool

def test_exec_tool_simple_print():
    code = 'print("hello-from-exec-tool")'
    res = exec_tool(code, timeout=3)
    assert isinstance(res, dict)
    assert res.get("success") is True
    assert "hello-from-exec-tool" in res.get("stdout", "")

def test_exec_tool_timeout():
    code = 'import time\\ntime.sleep(10)\\nprint("done")'
    res = exec_tool(code, timeout=1)
    assert isinstance(res, dict)
    assert res.get("success") is False or "TimeoutExpired" in (res.get("stderr") or "")

def test_search_tool_basic():
    q = "python programming"
    res = search_tool(q)
    assert isinstance(res, dict)
    assert res["query"] == q
    assert "results" in res
    assert isinstance(res["results"], list)
