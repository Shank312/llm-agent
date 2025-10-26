

# llm-agent/src/run_agent.py
import argparse
import json
import textwrap
import sys
from typing import Dict, Any


def local_mini_agent(prompt: str) -> Dict[str, Any]:
    """
    Small deterministic mini-agent for common coding prompts.
    Returns a dict: {response: str, code: str (if any), run_command: str (if any)}
    """
    p = prompt.lower().strip()

    # Reverse string
    if "reverse" in p and "string" in p:
        code = textwrap.dedent(
            '''
            def reverse_string(s: str) -> str:
                """
                Return the reverse of the input string.
                Example:
                    >>> reverse_string("abc")
                    "cba"
                """
                return s[::-1]


            if __name__ == "__main__":
                # simple interactive demo
                inp = input("Enter string to reverse: ")
                print(reverse_string(inp))
            '''
        ).strip()
        run_cmd = 'python reverse_string_demo.py  # save the code to this filename and run'
        resp = "Generated a short Python function `reverse_string(s)` and a small demo."
        return {"response": resp, "code": code, "run_command": run_cmd}

    # Fibonacci (small)
    if "fibonacci" in p:
        code = textwrap.dedent(
            '''
            def fib(n: int) -> int:
                """Return the n-th Fibonacci (0-indexed)."""
                if n < 2:
                    return n
                a, b = 0, 1
                for _ in range(2, n+1):
                    a, b = b, a + b
                return b


            if __name__ == "__main__":
                n = int(input("n: "))
                print(fib(n))
            '''
        ).strip()
        run_cmd = 'python fibonacci_demo.py'
        return {"response": "Generated Fibonacci function.", "code": code, "run_command": run_cmd}

    # Factorial
    if "factorial" in p:
        code = textwrap.dedent(
            '''
            def factorial(n: int) -> int:
                if n < 2:
                    return 1
                res = 1
                for i in range(2, n+1):
                    res *= i
                return res


            if __name__ == "__main__":
                n = int(input("n: "))
                print(factorial(n))
            '''
        ).strip()
        run_cmd = 'python factorial_demo.py'
        return {"response": "Generated factorial function.", "code": code, "run_command": run_cmd}

    # Hello world fallback
    code = 'print("Hello from the local mini-agent!")'
    run_cmd = 'python hello_demo.py'
    return {"response": "No specific intent recognized; returning a hello-world snippet.", "code": code, "run_command": run_cmd}


def main():
    parser = argparse.ArgumentParser(description="Run a small LLM agent (langchain) with tools.")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt for the agent.")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON result.")
    args = parser.parse_args()

    # Lazy import to avoid heavy deps at import time
    from .agent import run_prompt

    # Run the (LangChain) agent wrapper
    result = run_prompt(args.prompt, return_raw=True)

    # If LangChain isn't available or returned a fallback, use local mini-agent to produce helpful code
    if isinstance(result, dict) and result.get("fallback") is True:
        mini = local_mini_agent(args.prompt)
        # prefer to return the mini-agent's code as the main 'response' for CLI users
        output = {
            "prompt": args.prompt,
            "agent_fallback": True,
            "mini_agent": mini,
            "original_fallback_message": result.get("response"),
            "timestamp": result.get("timestamp"),
        }
        if args.raw:
            print(json.dumps(output, indent=2, ensure_ascii=False))
            return 0
        # Nicely print a developer-friendly output
        print("=== Local mini-agent response ===\n")
        print(mini.get("response"))
        print("\n=== Code ===\n")
        print(mini.get("code"))
        print("\n=== Run ===\n")
        print(mini.get("run_command"))
        print("\n=== Original agent fallback ===\n")
        print(result.get("response"))
        return 0

    # If the LangChain agent produced something (non-fallback), print it
    if args.raw:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print("=== Agent response ===")
    print(result.get("response") or "NO RESPONSE")
    print("\n=== metadata ===")
    meta = {k: v for k, v in result.items() if k not in ("response",)}
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

