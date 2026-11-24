#!/usr/bin/env python3
"""Derive concept-only logo treatments from the ORIGINAL Lucky Domains logo files.

Inputs are read-only copies of files from kenashe/luckydomains (assets/).
Nothing is written back to production. Geometry is never altered: only the
navy channel is recolored for dark backgrounds (per-pixel unmixing of the two
brand colors), so every edge and proportion matches the original.

Usage: python3 tools/make_assets.py /path/to/luckydomains/assets
"""
import sys, shutil
from pathlib import Path
from PIL import Image
import numpy as np

SRC = Path(sys.argv[1]); OUT = Path(__file__).resolve().parent.parent / "shared" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
NAVY = np.array([12, 35, 64], float); GREEN = np.array([22, 199, 132], float)

def recolor(img, navy_to=None, green_to=None):
    a = np.asarray(img.convert("RGBA")).astype(float)
    rgb = a[..., :3]
    axis = GREEN - NAVY
    t = np.clip(((rgb - NAVY) @ axis) / (axis @ axis), 0, 1)[..., None]   # 0 = navy, 1 = green
    n = np.array(navy_to, float) if navy_to is not None else NAVY
    g = np.array(green_to, float) if green_to is not None else GREEN
    out = a.copy(); out[..., :3] = n * (1 - t) + g * t
    return Image.fromarray(out.round().astype("uint8"), "RGBA")

WARM = (236, 231, 220)
for name in ("logo-wordmark.png", "logo-icon.png"):
    im = Image.open(SRC / name)
    stem = name[:-4]
    shutil.copy(SRC / name, OUT / name)                                   # 1. original, untouched
    recolor(im, navy_to=WARM).save(OUT / f"{stem}-reversed.png", optimize=True)        # 2. reversed
    recolor(im, navy_to=WARM, green_to=WARM).save(OUT / f"{stem}-mono-light.png", optimize=True)  # 3. mono light
    recolor(im, green_to=NAVY).save(OUT / f"{stem}-mono-ink.png", optimize=True)       # 4. mono ink
# compact icon at header size
Image.open(SRC / "logo-icon.png").resize((128, 128), Image.LANCZOS).save(OUT / "logo-icon-128.png", optimize=True)
recolor(Image.open(SRC / "logo-icon.png"), navy_to=WARM).resize((128, 128), Image.LANCZOS).save(OUT / "logo-icon-reversed-128.png", optimize=True)
for f in ("favicon.ico", "favicon-32.png", "apple-touch-icon.png", "ken-ashe-2026-square.jpg"):
    shutil.copy(SRC / f, OUT / f)
print("assets written to", OUT)
