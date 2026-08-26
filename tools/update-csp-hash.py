#!/usr/bin/env python3
"""Re-stamp vercel.json's script hash after index.html changes.

The Content-Security-Policy allows exactly one inline script: the one in
index.html, named by its SHA-256. Edit that script without re-running this and
the browser refuses to execute it, so the page loads and then does nothing.

    python3 tools/update-csp-hash.py
"""
import base64, hashlib, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / 'index.html').read_text()
cfg_path = root / 'vercel.json'
cfg = cfg_path.read_text()

scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
if len(scripts) != 1:
    sys.exit('expected exactly one inline <script>, found %d' % len(scripts))

want = 'sha256-' + base64.b64encode(hashlib.sha256(scripts[0].encode()).digest()).decode()
have = re.search(r"'(sha256-[^']+)'", cfg)
if not have:
    sys.exit('no script hash found in vercel.json')

if have.group(1) == want:
    print('hash already current:', want)
else:
    cfg_path.write_text(cfg.replace(have.group(1), want))
    print('hash updated:', have.group(1), '->', want)
