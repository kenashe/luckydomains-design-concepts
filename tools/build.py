#!/usr/bin/env python3
"""Regenerate every concept page from shared/content.json.

    python3 tools/build.py

Output is plain static HTML committed to the repository. GitHub Pages serves the
files as they are: there is no build step on the host.
"""
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

for mod in ("concept_a", "concept_a_v2", "concept_b", "concept_c", "review", "p2_a", "p2_b", "p2_c", "p2_review"):
    try:
        m = importlib.import_module(mod)
    except ModuleNotFoundError as e:
        if e.name != mod:
            raise
        continue
    m.build()
    print("built", mod)
