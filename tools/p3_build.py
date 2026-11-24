"""Build only version 3 (content, three concepts, the refined concept C, review pages)."""
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3_content  # noqa: F401  (writes phase-3/shared/content.json)
for m in ("p3_a", "p3_b", "p3_c", "p3_r", "p3_review"):
    try:
        mod = importlib.import_module(m)
    except ModuleNotFoundError as e:
        if e.name != m: raise
        continue
    mod.build(); print("built", m)
