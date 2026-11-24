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
STAGES = ("production-candidate", "digital-presence-production-candidate")   # exported staging copies, see tools/export_staging.py and tools/dp_export.py
SITE_PREFIX = "/luckydomains-design-concepts/"
for p in pages:
    s = p.read_text(); rel = p.relative_to(ROOT)
    staged = rel.parts[0] in STAGES
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
    p2c = (rel.parts[0] == "phase-2" and len(rel.parts) > 2 and rel.parts[1] in ("original-evolved", "editorial-authority", "intelligent-presence")) or \
          (rel.parts[0] == "phase-3" and len(rel.parts) > 2 and rel.parts[1] in ("original-evolved", "editorial", "interactive", "interactive-refined"))
    if (str(rel).startswith("concept-") or p2c) and NOTICE not in s: fails.append(f"{rel}: review notice missing")
    if p2c and "logo-wordmark.png" not in s: fails.append(f"{rel}: original logo missing")
    if p2c and not re.search(r"Domain Acquisition", s): fails.append(f"{rel}: domain acquisition not linked")
    if p2c and re.search(r"\bVentures\b", s): fails.append(f"{rel}: Phase 2 must not use Ventures navigation")
    if rel.parts[0] in ("phase-2", "phase-3"):
        for m in re.finditer(r"guarantee(d|s)? (rankings|citations|a Knowledge Panel|AI)", s, re.I):
            before = s[max(0, m.start() - 40):m.start()].lower()
            if not re.search(r"\b(no|not|never|cannot|can't|nobody)\b", before): fails.append(f"{rel}: unqualified guarantee language")
    if str(rel).startswith("concept-") and "logo-wordmark" not in s: fails.append(f"{rel}: Lucky Domains logo missing")
    if str(rel).startswith("concept-") and rel.parent.parent == Path(".") and "logo-wordmark.png" not in s: fails.append(f"{rel}: original full-color logo missing from concept home page")
    if str(rel).startswith("concept-") and not re.search(r"[Dd]omain acquisition", s): fails.append(f"{rel}: domain acquisition not mentioned")
    if rel.parts[:2] == ("phase-3", "interactive-refined"):          # the refinement has no portfolio
        if re.search(r'href="[^"]*work/', s): fails.append(f"{rel}: refined concept links to a Work page")
        if re.search(r"case stud|portfolio|testimonial|Selected work", re.sub(r'href="[^"]*"', "", s), re.I): fails.append(f"{rel}: refined concept mentions a portfolio or case study")
        if "<form" in s and "data-inert" not in s: fails.append(f"{rel}: form is not inert")
    if re.search(r"<form[^>]*\saction=", s): fails.append(f"{rel}: form has an action")
    if re.search(r'type="submit"', s): fails.append(f"{rel}: submit button present")
    for m in re.finditer(r"<(?:input|textarea|select)[^>]*\sname=\"([^\"]+)\"", s):
        if m.group(1) not in ("regarding", "stuck") and not re.fullmatch(r"dpc-\d+", m.group(1)): fails.append(f"{rel}: named form control {m.group(1)}")
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
for STAGE in STAGES:
    if not (ROOT / STAGE).exists(): continue
    if "api.web3forms.com" in (ROOT / STAGE / "js" / "main.js").read_text(): fails.append(f"{STAGE}: staging script still names the form endpoint")
    for f in ("sitemap.xml", "robots.txt"):
        if (ROOT / STAGE / f).exists(): fails.append(f"{STAGE}: staging must not carry {f}")
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
