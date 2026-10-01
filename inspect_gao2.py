# -*- coding: utf-8 -*-
import re, glob, html

def to_text(s):
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>|</div>|</li>|</tr>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\u00a0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()

target = None
for fp in glob.glob("data/raw/profiles/ep-*.html"):
    t = open(fp, encoding="utf-8", errors="ignore").read()
    if "高河伟" in t and "gwbgs" in t:
        target = fp
        break
t = open(target, encoding="utf-8", errors="ignore").read()

# menu items
menu = re.findall(r'<div class="text">(.*?)</div>', t)
# content panels
panels = re.findall(r'<div class="tli-content[^"]*">(.*?)</div>\s*(?=<div class="tli-content|</div>\s*</div>|$)', t, flags=re.S)
print("menu:", menu)
print("panels:", len(panels))
out = {}
for i, (m, pan) in enumerate(zip(menu, panels)):
    out[m] = to_text(pan)[:300]
import json
json.dump(out, open("qc_gao_panels.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# email candidates
emails = re.findall(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}', t)
print("emails:", set(emails))
