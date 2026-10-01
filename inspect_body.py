# -*- coding: utf-8 -*-
import re, json, os, html
PROF = "data/raw/profiles"

def to_text(s):
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>|</div>|</tr>|</li>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\u00a0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()

# take a physics profile WITHOUT xq-title and show its body text
man = json.load(open("profile_manifest.json", encoding="utf-8"))
def body_text(c):
    # try to cut off the header/nav: start after the breadcrumb / at first meaningful marker
    i = c.find('teacher-name')
    if i < 0:
        i = c.find('teach-top')
    return to_text(c[i:]) if i > 0 else to_text(c)

samples = ["phys-陈难先", "phys-薛其坤", "phys-段文晖"]
for s in samples:
    fp = "data/raw/profiles/%s.html" % s
    if not os.path.exists(fp):
        continue
    c = open(fp, encoding="utf-8", errors="ignore").read()
    t = body_text(c)
    with open("tmp_body_%s.txt" % s, "w", encoding="utf-8") as f:
        f.write(t[:3000])
    print("wrote", s, len(t))
