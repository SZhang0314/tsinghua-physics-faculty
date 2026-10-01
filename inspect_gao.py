# -*- coding: utf-8 -*-
import re, glob, os
# find the 高河伟 profile
target = None
for fp in glob.glob("data/raw/profiles/ep-*.html"):
    t = open(fp, encoding="utf-8", errors="ignore").read()
    if "高河伟" in t and "gwbgs" in t:
        target = fp
        break
print("target", target)
t = open(target, encoding="utf-8", errors="ignore").read()
# find the research tab structure - look for onclick tabs or iframe/ajax
for pat in [r'tab', r'iframe', r'研究概况', r'研究方向', r'\.js', r'ajax', r'load\(']:
    print(pat, len(re.findall(pat, t)))
# dump body region
i = t.find('研究概况')
with open("tmp_gao.txt", "w", encoding="utf-8") as f:
    f.write(t[i-1500:i+2500])
print("idx", i, "len", len(t))
