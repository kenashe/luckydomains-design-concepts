"""Shared helpers for the three Phase 2 concepts. Content comes from phase-2/shared/content.json.
Phase 1 (tools/lib.py, shared/content.json) is not read or changed by anything here."""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = json.loads((ROOT / "phase-2" / "shared" / "content.json").read_text())
E = html.escape
S = {s["id"]: s for s in C["services"]}
LAYER = {l["id"]: l for l in C["stack"]}
NOTICE = "Design concept only. Not the live Lucky Domains website."
PAGES = [("", "Home"), ("services/", "Services"), ("services/website-design/", "Website Design & Development"),
         ("services/search-ai-visibility/", "Search & AI Visibility"), ("services/domain-identity/", "Domain Strategy & Digital Identity"),
         ("work/", "Work")]


class Ctx:
    def __init__(self, concept, path):
        self.concept, self.path = concept, path
        d = path.count("/")
        self.c = "../" * d or "./"                 # concept root
        self.r = "../" * (d + 2)                   # repository root (phase-2/<concept>/...)
    def to(self, p=""):
        return (self.c + p) if p else self.c
    def asset(self, name):
        return f"{self.r}shared/assets/{name}"
    def font(self, name):
        return f"{self.r}shared/fonts/{name}"
    def svc(self, sid):
        s = S[sid]
        return self.to("services/" + s["page"]) + (f"#{s['anchor']}" if s["anchor"] else "")
    def home(self, frag):
        return self.to() + frag if self.path else frag
    def cur(self, p):
        return ' aria-current="page"' if self.path == p or (p and p != "services/" and self.path.startswith(p)) or (p == "services/" and self.path.startswith("services/")) else ""


def head(ctx, title, desc, css, preload=()):
    pl = "".join(f'<link rel="preload" href="{ctx.font(f)}" as="font" type="font/woff2" crossorigin>' for f in preload)
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
<link rel="stylesheet" href="{ctx.c}css/style.css">
<script>document.documentElement.className='js'</script>
</head>"""


def notice(ctx, label):
    return (f'<aside class="review" aria-label="Review notice"><span>{NOTICE} <span class="rv-x">Phase 2, {E(label)}.</span></span> '
            f'<a href="{ctx.r}phase-2/">Phase 2 concepts</a></aside>')


def nav_links(ctx, cls_menu="menu"):
    """Primary navigation items. Services has a disclosure menu; the link itself goes to the overview."""
    items = ""
    for n in C["nav"]:
        if n.get("menu"):
            sub = "".join(f'<li><a href="{ctx.svc(s["id"])}">{E(s["name"])}</a></li>' for s in C["services"])
            items += (f'<li class="has-menu"><a href="{ctx.to(n["href"])}"{ctx.cur("services/")}>{E(n["label"])}</a>'
                      f'<button class="menu-btn" type="button" aria-expanded="false" aria-controls="m-svc"><span class="sr">Show service pages</span></button>'
                      f'<ul class="{cls_menu}" id="m-svc"><li><a href="{ctx.to("services/")}">All services</a></li>{sub}</ul></li>')
        elif n["href"].startswith("#"):
            items += f'<li><a href="{ctx.home(n["href"])}">{E(n["label"])}</a></li>'
        else:
            items += f'<li><a href="{ctx.to(n["href"])}"{ctx.cur(n["href"])}>{E(n["label"])}</a></li>'
    return items


def field(label, kind="text", options=None):
    """Form control with no name attribute: it cannot be serialized or submitted."""
    if kind == "textarea":
        ctl = '<textarea rows="4" autocomplete="off"></textarea>'
    elif kind == "select":
        ctl = "<select>" + "".join(f"<option>{E(o)}</option>" for o in options) + "</select>"
    else:
        ctl = f'<input type="{kind}" autocomplete="off">'
    return f"<label><span>{E(label)}</span>{ctl}</label>"


def contact_form(cls="cf"):
    c = C["contact"]
    return (f'<form class="{cls}" novalidate data-inert>{field("Name")}{field("Email", "email")}'
            f'{field("What is this about?", "select", c["paths"])}{field("Tell Ken what you are working on", "textarea")}'
            f'<button type="button" class="btn btn-p">Send to Ken</button><p class="cf-note" role="status">{E(c["notice"])}</p></form>')


def write(rel, text):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text.strip() + "\n")


def scripts(ctx):
    return f'<script src="{ctx.r}phase-2/shared/p2.js" defer></script>\n<script src="{ctx.c}js/main.js" defer></script>'
