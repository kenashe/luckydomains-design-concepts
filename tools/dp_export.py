#!/usr/bin/env python3
"""Export a noindex staging copy of the digital presence production candidate.

    python3 tools/dp_export.py /path/to/luckydomains-checkout

The checkout must be on the branch digital-presence-production-candidate of
kenashe/luckydomains, with everything committed. That branch is the source of
truth. This script never writes to it. It copies the site files into
digital-presence-production-candidate/ in this repository and applies ONLY
these staging transformations:

  1. Base path. Root-absolute links (href="/x", src="/x", meta refresh and
     location.replace targets, the manifest start_url) get the prefix
     /luckydomains-design-concepts/digital-presence-production-candidate. The
     presence map keeps its links in a small JSON block, so the "href" and
     "icon" values in that block get the same prefix.
  2. Robots. Every page gets <meta name="robots" content="noindex,nofollow,noarchive">,
     replacing any existing robots meta. This repository's robots.txt already
     disallows all crawling.
  3. Canonical and social URLs in <head> (canonical, og:url, og:image,
     twitter:image) point at the staging URL, so no staging page claims a
     production address. JSON-LD and body links are left exactly as in production.
  4. Review notice. A slim bar is inserted at the top of every page.
  5. Contact form. The Web3Forms access key is removed from the HTML, the
     endpoint constant in js/main.js is replaced, and staging.js blocks submit
     in the capture phase and shows a review message. Nothing can be sent.
  6. Omitted files: CNAME, robots.txt, sitemap.xml, documentation, tests,
     scripts, .github, assets/source.

Run it again after any change to the branch. Never edit the exported folder by
hand. The earlier Venture Lab export in production-candidate/ is an archive and
is not touched by this script (tools/export_staging.py produced it).
"""
import re, sys, shutil, subprocess, hashlib, json
from pathlib import Path

SRC = Path(sys.argv[1]).resolve()
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "digital-presence-production-candidate"
BASE = "/luckydomains-design-concepts/digital-presence-production-candidate"
BRANCH = "digital-presence-production-candidate"
HOST = "https://kenashe.github.io"
PROD = "https://luckydomains.io"
KEY_RE = re.compile(r'data-access-key="[^"]*"')
NOTICE = ('<aside class="stg-note" aria-label="Staging notice" style="margin:0;padding:8px 16px;background:#f3efe6;color:#0c2340;'
          'font:500 13px/1.5 system-ui,sans-serif;display:flex;flex-wrap:wrap;gap:4px 16px;justify-content:center;text-align:center">'
          '<span>Staging review. Not the live Lucky Domains website. Forms are disabled.</span> '
          f'<a href="{BASE}/review/" style="color:#0c2340;font-weight:700;display:inline-block;padding:4px 0">Review notes</a></aside>')

branch = subprocess.run(["git", "-C", str(SRC), "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
commit = subprocess.run(["git", "-C", str(SRC), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(["git", "-C", str(SRC), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
if branch != BRANCH: sys.exit(f"Refusing: the checkout is on {branch!r}. Staging is exported from {BRANCH}.")
if dirty: sys.exit("Refusing: the checkout has uncommitted changes. Commit first so staging matches a commit.")

keep = {}
for sub in ("review",):                                   # generated review material survives a re-export
    if (OUT / sub).exists(): keep[sub] = OUT / sub
tmp = ROOT / ".dp-keep"
if tmp.exists(): shutil.rmtree(tmp)
tmp.mkdir()
for k, p in keep.items(): shutil.move(str(p), str(tmp / k))
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
for k in keep: shutil.move(str(tmp / k), str(OUT / k))
shutil.rmtree(tmp)

SKIP_DIRS = {".git", ".github", "docs", "tests", "scripts"}
SKIP_FILES = {"CNAME", "robots.txt", "sitemap.xml", ".nojekyll", ".gitignore", ".env.example"}
files = []
for p in sorted(SRC.rglob("*")):
    rel = p.relative_to(SRC)
    if not p.is_file() or rel.parts[0] in SKIP_DIRS or rel.name in SKIP_FILES or rel.suffix == ".md": continue
    if rel.parts[:2] == ("assets", "source"): continue
    files.append(rel)


def html(text, rel):
    text = re.sub(r'<meta name="robots"[^>]*>\n?', "", text)
    text = text.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex,nofollow,noarchive">', 1)
    head, sep, body = text.partition("</head>")
    for attr in ('rel="canonical" href="', 'property="og:url" content="', 'property="og:image" content="', 'name="twitter:image" content="'):
        head = head.replace(attr + PROD, attr + HOST + BASE)
    text = head + sep + body
    text = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{BASE}/', text)
    text = re.sub(r'content="0; url=/', f'content="0; url={BASE}/', text)
    text = re.sub(r'window\.location\.replace\("/', f'window.location.replace("{BASE}/', text)
    text = re.sub(r'(<script type="application/json" class="pm-data">)(.*?)(</script>)',
                  lambda m: m.group(1) + re.sub(r'"(href|icon)": "/', lambda k: f'"{k.group(1)}": "{BASE}/', m.group(2)) + m.group(3), text, flags=re.S)
    if '<a class="skip-link"' in text:      # keep the skip link first in the page
        text = re.sub(r'(<a class="skip-link"[^>]*>.*?</a>)', lambda m: m.group(1) + "\n" + NOTICE, text, count=1)
    else:
        text = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + NOTICE, text, count=1)
    if KEY_RE.search(text):
        text = KEY_RE.sub('data-access-key="" data-staging="true"', text)
    text = text.replace(f'<script src="{BASE}/js/main.js" defer></script>', f'<script src="{BASE}/staging.js" defer></script>\n<script src="{BASE}/js/main.js" defer></script>')
    return text


for rel in files:
    dst = OUT / rel; dst.parent.mkdir(parents=True, exist_ok=True)
    if rel.suffix == ".html":
        dst.write_text(html((SRC / rel).read_text(), rel))
    elif rel.as_posix() == "js/main.js":
        dst.write_text((SRC / rel).read_text().replace("https://api.web3forms.com/submit", "about:blank#staging-form-disabled"))
    elif rel.name == "site.webmanifest":
        m = json.loads((SRC / rel).read_text()); m["start_url"] = BASE + "/"; m["name"] += " (staging)"
        dst.write_text(json.dumps(m, indent=2) + "\n")
    else:
        shutil.copyfile(SRC / rel, dst)

(OUT / "staging.js").write_text("""/* Staging only. Blocks the contact form before the site script can send anything. */
document.addEventListener('submit', function (e) {
  e.preventDefault(); e.stopImmediatePropagation();
  var s = document.getElementById('form-status');
  if (s) { s.textContent = 'Review environment. This form is disabled here and nothing was collected, stored, or sent.'; s.className = 'form-status show err'; }
}, true);
""")

# ---- self-check: fail loudly if a protection is missing
bad = []
for p in OUT.rglob("*.html"):
    if "review" in p.relative_to(OUT).parts[:1]: continue
    t = p.read_text()
    if '<meta name="robots" content="noindex,nofollow,noarchive">' not in t: bad.append(f"{p}: not noindex")
    if "Staging review. Not the live Lucky Domains website." not in t: bad.append(f"{p}: no staging notice")
    if re.search(r'(href|src)="/(?!luckydomains-design-concepts/)', t): bad.append(f"{p}: root link without the staging prefix")
    if re.search(r'data-access-key="[^"]+"', t): bad.append(f"{p}: access key present")
    if re.search(r'"(href|icon)": "/(?!luckydomains-design-concepts/)', t): bad.append(f"{p}: map link without the staging prefix")
if "api.web3forms.com" in (OUT / "js" / "main.js").read_text(): bad.append("main.js still names the form endpoint")
for f in ("CNAME", "sitemap.xml", "robots.txt"):
    if (OUT / f).exists(): bad.append(f"{f} must not be exported")
if bad: sys.exit("EXPORT FAILED\n  " + "\n  ".join(bad))

pages = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*.html") if p.relative_to(OUT).parts[0] != "review")
digest = hashlib.sha256("".join(hashlib.sha256((SRC / r).read_bytes()).hexdigest() for r in files).encode()).hexdigest()[:16]
(OUT / "STAGING.json").write_text(json.dumps({"source_repository": "kenashe/luckydomains", "source_branch": branch, "source_commit": commit,
    "source_digest": digest, "files": len(files), "pages": pages,
    "transformations": ["base path prefix", "noindex,nofollow,noarchive on every page", "head canonical and social URLs point at staging",
                        "presence-map links prefixed", "staging notice bar", "contact form disabled (key removed, endpoint replaced, submit blocked)",
                        "CNAME, robots.txt, sitemap.xml, docs, tests, scripts and assets/source omitted"]}, indent=2) + "\n")
print(f"exported {len(files)} files ({len(pages)} pages) from {branch}@{commit[:10]} to {OUT.relative_to(ROOT)}/")
