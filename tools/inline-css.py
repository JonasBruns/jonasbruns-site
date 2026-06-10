#!/usr/bin/env python3
"""Inline styles.css into index.html's critical-CSS block.

styles.css is the single source of truth (the sub-pages link it directly).
The homepage inlines a copy to avoid a render-blocking stylesheet request.
Run this after editing styles.css:

    python tools/inline-css.py

It rewrites whatever sits between the <!-- inline-css:start --> and
<!-- inline-css:end --> markers in index.html. Idempotent.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
css = (ROOT / "styles.css").read_text(encoding="utf-8").strip()
html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")

block = "  <!-- inline-css:start -->\n  <style>\n" + css + "\n  </style>\n  <!-- inline-css:end -->"
new_html, n = re.subn(
    r"  <!-- inline-css:start -->.*?<!-- inline-css:end -->",
    lambda _m: block,
    html,
    flags=re.DOTALL,
)
if n != 1:
    sys.exit(f"error: expected exactly 1 inline-css marker block, found {n}")

if new_html != html:
    html_path.write_text(new_html, encoding="utf-8")
    print(f"inlined {len(css)} bytes of CSS into index.html")
else:
    print("index.html already up to date")
