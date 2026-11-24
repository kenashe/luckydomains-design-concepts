#!/usr/bin/env python3
"""Static safety and integrity checks for the concept site. No dependencies.

    python3 tools/verify.py            # static checks
    python3 tools/verify.py --links    # also request every external URL once
"""
import re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTICE = "Design concept only. Not the live Lucky Domains website."
fails, ext = [], set()
pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
STAGE = "production-candidate"
SITE_PREFIX = "/luckydomains-design-concepts/"
for p in pages:
    s = p.read_text(); rel = p.relative_to(ROOT)
    staged = rel.parts[0] == STAGE                    # exported production candidate, see tools/export_staging.py
    stub = 'http-equiv="refresh"' in s
    if staged:
        if '<meta name="robots" content="noindex,nofollow,noarchive">' not in s: fails.append(f"{rel}: staging page is not noindex")
        if rel.parts[1:2] != ("review",):
            if "Staging review. Not the live Lucky Domains website." not in s: fails.append(f"{rel}: staging notice missing")
            if re.search(r'data-access-key="[^"]+"', s): fails.append(f"{rel}: staging form still carries an access key")
            if "<form" in s and "staging.js" not in s: fails.append(f"{rel}: staging form is not blocked")
        if re.search(r"<form[^>]*\saction=", s): fails.append(f"{rel}: form has an action")
        if not stub and s.count("<h1") != 1: fails.append(f"{rel}: expected exactly one h1")
        for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
            u = m.group(1)
            if u.startswith(("http://", "https://")): ext.add(u); continue
            if u.startswith(("mailto:", "#", "data:")): continue
            if u.startswith(SITE_PREFIX): t = ROOT / u[len(SITE_PREFIX):].split("#")[0].split("?")[0]
            elif u.startswith("/"): fails.append(f"{rel}: root link escapes staging {u}"); continue
            else: t = (p.parent / u.split("#")[0].split("?")[0]).resolve()
            if t.is_dir(): t = t / "index.html"
            if not t.exists(): fails.append(f"{rel}: broken internal link {u}")
        continue
    if '<meta name="robots" content="noindex,nofollow,noarchive">' not in s: fails.append(f"{rel}: robots meta missing")
    if str(rel).startswith("concept-") and NOTICE not in s: fails.append(f"{rel}: review notice missing")
    if str(rel).startswith("concept-") and "logo-wordmark" not in s: fails.append(f"{rel}: Lucky Domains logo missing")
    if str(rel).startswith("concept-") and rel.parent.parent == Path(".") and "logo-wordmark.png" not in s: fails.append(f"{rel}: original full-color logo missing from concept home page")
    if str(rel).startswith("concept-") and not re.search(r"[Dd]omain acquisition", s): fails.append(f"{rel}: domain acquisition not mentioned")
    if re.search(r"<form[^>]*\saction=", s): fails.append(f"{rel}: form has an action")
    if re.search(r'type="submit"', s): fails.append(f"{rel}: submit button present")
    for m in re.finditer(r"<(?:input|textarea|select)[^>]*\sname=\"([^\"]+)\"", s):
        if m.group(1) != "regarding": fails.append(f"{rel}: named form control {m.group(1)}")
    if re.search(r"googletagmanager|google-analytics|gtag\(|plausible|web3forms|formspree|api[_-]?key", s, re.I): fails.append(f"{rel}: analytics, form endpoint or key reference")
    if s.count("<h1") != 1: fails.append(f"{rel}: expected exactly one h1, found {s.count('<h1')}")
    for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
        u = m.group(1)
        if u.startswith(("http://", "https://")): ext.add(u); continue
        if u.startswith(("mailto:", "#", "data:")): continue
        t = (p.parent / u.split("#")[0].split("?")[0]).resolve()
        if t.is_dir(): t = t / "index.html"
        if not t.exists(): fails.append(f"{rel}: broken internal link {u}")
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix in {".html", ".css", ".js", ".json", ".md", ".py", ".txt"} and ".git" not in p.parts:
        t = p.read_text()
        for ch, nm in (("\u2014", "em dash"), ("\u2013", "en dash")):
            if ch in t: fails.append(f"{p.relative_to(ROOT)}: contains an {nm}")
if list(ROOT.rglob("CNAME")): fails.append("CNAME file present: this repo must not claim a custom domain")
if (ROOT / STAGE).exists():
    if "api.web3forms.com" in (ROOT / STAGE / "js" / "main.js").read_text(): fails.append("staging script still names the form endpoint")
    for f in ("sitemap.xml", "robots.txt"):
        if (ROOT / STAGE / f).exists(): fails.append(f"staging must not carry {f}")
if "Disallow: /" not in (ROOT / "robots.txt").read_text(): fails.append("robots.txt does not disallow crawling")
print(f"{len(pages)} pages checked, {len(ext)} distinct external URLs")
if "--links" in sys.argv:
    for u in sorted(ext):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (concept link check)"}), timeout=20)
            code = r.status
        except Exception as e:
            code = getattr(e, "code", str(e)[:60])
        print(f"  {code}  {u}")
        if code not in (200, 999, 403, 429) and "/production-candidate/" not in u: fails.append(f"external link {u} returned {code}")
print("FAIL" if fails else "PASS"); [print("  -", f) for f in fails]
sys.exit(1 if fails else 0)
