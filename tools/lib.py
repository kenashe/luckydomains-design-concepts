"""Shared helpers for the concept generator. No dependencies beyond the standard library."""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = json.loads((ROOT / "shared" / "content.json").read_text())
E = html.escape
V = {v["id"]: v for v in C["ventures"]}
NOTICE = "Design concept only. Not the live Lucky Domains website."
PAGES = [("ventures/", "Ventures"), ("services/", "Services"), ("about/", "About"),
         ("founder/", "Founder"), ("news/", "Updates"), ("contact/", "Contact")]


class Ctx:
    """Relative-path context for one page. depth = folders below the concept root."""
    def __init__(self, concept_dir, path):
        self.dir = concept_dir
        self.path = path                      # "" for home, "ventures/", "ventures/zerohuman/"
        d = path.count("/")
        self.c = "../" * d or "./"            # to the concept root
        self.r = "../" * (d + 1)              # to the repository root
    def to(self, p=""):                       # link inside the concept
        return (self.c + p) if p else self.c
    def asset(self, name):
        return f"{self.r}shared/assets/{name}"
    def cur(self, p):
        return ' aria-current="page"' if (self.path == p or (p and self.path.startswith(p))) else ""


def head(ctx, title, desc, css, preload=()):
    pl = "".join(f'<link rel="preload" href="{ctx.r}shared/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in preload)
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="icon" href="{ctx.asset('favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{ctx.asset('favicon-32.png')}">
<link rel="apple-touch-icon" href="{ctx.asset('apple-touch-icon.png')}">
{pl}
<link rel="stylesheet" href="{ctx.c}{css}">
<script>document.documentElement.className='js'</script>
</head>"""


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n")


def status_slug(s):
    return s.lower().replace(" ", "-")


def field(label, long=False, type_="text"):
    """A form control with no name attribute: it cannot be serialized or submitted."""
    ctl = '<textarea rows="4" autocomplete="off"></textarea>' if long else f'<input type="{type_}" autocomplete="off">'
    return f"<label><span>{E(label)}</span>{ctl}</label>"


def is_long(label):
    return label == "Your message" or "building" in label
