

# llm-agent/src/tools.py
import json
import os
import shlex
import subprocess
import tempfile
import time
from typing import Dict, Any, Optional

import requests

# For Unix resource limits in the executor
try:
    import resource
except Exception:
    resource = None  # resource may not be available on Windows


def search_tool(query: str, max_results: int = 5, timeout: int = 5) -> Dict[str, Any]:
    """
    Minimal web-search using DuckDuckGo Instant Answer API.
    If network fails, returns a graceful placeholder.

    Returns a dict with keys: query, timestamp, source, results (list of dicts).
    Each result dict: {title, snippet, url}
    """
    endpoint = "https://api.duckduckgo.com/"
    payload = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
    ts = time.time()
    try:
        r = requests.get(endpoint, params=payload, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        results = []

        # DuckDuckGo instant answer returns 'RelatedTopics' which may contain topics
        topics = data.get("RelatedTopics", [])
        # sometimes AbstractText/title/url available
        if data.get("AbstractText"):
            results.append({"title": data.get("Heading") or query,
                            "snippet": data.get("AbstractText"),
                            "url": data.get("AbstractURL") or ""})
        # grab up to max_results from RelatedTopics
        for t in topics:
            if len(results) >= max_results:
                break
            if isinstance(t, dict):
                title = t.get("Text") or t.get("Name") or ""
                snippet = t.get("Text") or ""
                url = t.get("FirstURL") or ""
                results.append({"title": title, "snippet": snippet, "url": url})
            elif isinstance(t, list):
                for sub in t:
                    if len(results) >= max_results:
                        break
                    results.append({
                        "title": sub.get("Text") or "",
                        "snippet": sub.get("Text") or "",
                        "url": sub.get("FirstURL") or ""
                    })
        # fallback if no results
        if not results:
            results = [{"title": f"No direct results for '{query}'",
                        "snippet": data.get("AbstractText") or "",
                        "url": ""}]
        out = {"query": query, "timestamp": ts, "source": "duckduckgo_instant", "results": results[:max_results]}
        return out
    except Exception as e:
        # fallback placeholder
        return {
            "query": query,
            "timestamp": ts,
            "source": "placeholder",
            "error": str(e),
            "results": [
                {"title": f"PLACEHOLDER: results for '{query}'",
                 "snippet": "Network lookup failed or blocked. Enable network or set ALLOW_WEB=1 to attempt searches.",
                 "url": ""}
            ],
        }


def _set_limits_cpu_mem():
    """
    Preexec function to set resource limits for subprocess (Unix).
    Limits:
      - CPU time: 5 seconds
      - Address space (virtual memory): 200MB
      - File size: 1MB
    """
    if resource is None:
        return
    # CPU seconds
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    except Exception:
        pass
    # Address space (virtual memory)
    try:
        mem_bytes = 200 * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    except Exception:
        pass
    # prevent creation of big files
    try:
        resource.setrlimit(resource.RLIMIT_FSIZE, (1 * 1024 * 1024, 1 * 1024 * 1024))
    except Exception:
        pass

def exec_tool(code: str,
              timeout: int = 4,
              capture_output: bool = True,
              python_binary: str | None = None) -> Dict[str, Any]:
    """
    Safely execute Python code in a sandboxed subprocess.
    Returns dict: {success, stdout, stderr, returncode, duration_seconds}
    Notes:
      - Uses resource limits on Unix via preexec_fn.
      - Runs with the same Python interpreter by default (sys.executable) so it works on Windows.
      - Uses a minimal environment.
      - DOES NOT guarantee absolute security — for production, use containers.
    """
    import sys as _sys
    start = time.time()
    # ensure we use the same Python interpreter if none specified (works on Windows)
    if python_binary is None:
        python_binary = _sys.executable or "python"
    # write code to temp file to avoid shell quoting issues
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as f:
        fname = f.name
        f.write(code)
    cmd = [python_binary, fname]

    # Minimal environment
    env = {"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            env=env,
            preexec_fn=_set_limits_cpu_mem if resource is not None else None,
            text=True,
        )
        try:
            out, err = proc.communicate(timeout=timeout)
            returncode = proc.returncode
            success = (returncode == 0)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
            returncode = proc.returncode
            success = False
            err = (err or "") + "\\n*** TimeoutExpired: process killed after %s seconds ***" % timeout
    except Exception as e:
        duration = time.time() - start
        # cleanup tmp file
        try:
            os.remove(fname)
        except Exception:
            pass
        return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1, "duration_seconds": duration}

    duration = time.time() - start
    # cleanup tmp file
    try:
        os.remove(fname)
    except Exception:
        pass

    return {"success": success, "stdout": out or "", "stderr": err or "", "returncode": returncode, "duration_seconds": duration}
