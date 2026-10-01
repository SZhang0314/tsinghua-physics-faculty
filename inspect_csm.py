# -*- coding: utf-8 -*-
import re, glob
target = None
for fp in glob.glob("data/raw/profiles/ep-*.html"):
    t = open(fp, encoding="utf-8", errors="ignore").read()
    if "陈少敏" in t and "4231" in t:
        target = fp
        break
t = open(target, encoding="utf-8", errors="ignore").read()
print("len", len(t))
for kw in ["tli-content", "text\">", "v_news_content", "研究领域", "研究方向", "xb-content", "ds-content"]:
    print(kw, t.count(kw))
# find main content markers
i = t.find("陈少敏")
with open("tmp_csm.txt", "w", encoding="utf-8") as f:
    f.write(t[i-300:i+3500])
