

python - <<'PY'
from pathlib import Path
p = Path('src/__init__.py')
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("""# Make `src` a python package so tests can import `src.*`
__all__ = []
""", encoding="utf-8")
print("wrote src/__init__.py")
PY

