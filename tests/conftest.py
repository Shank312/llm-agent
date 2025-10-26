# tests/conftest.py
# Ensure the repository-level `src` directory is first on sys.path during pytest runs.
import os
import sys

HERE = os.path.dirname(os.path.dirname(__file__))  # tests -> repo root
SRC = os.path.join(HERE, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
