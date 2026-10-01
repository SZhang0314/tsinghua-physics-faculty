# -*- coding: utf-8 -*-
import re
fp = "data/raw/profiles/ep-陈少敏_4231_htm.html"
import glob
for f in glob.glob("data/raw/profiles/ep-*4231*.html"):
    fp = f
t = open(fp, encoding="utf-8", errors="ignore").read()
menu = re.findall(r'<div class="text">(.*?)</div>', t)
print("MENU:", menu)
# panels with a permissive pattern
panels = re.findall(r'<div class="tli-content[^"]*">(.*?)</div>\s*</div>', t, flags=re.S)
print("panels(strict):", len(panels))
panels2 = re.findall(r'<div class="tli-content[^"]*">(.*?)(?=<div class="tli-content|</div>\s*</div>\s*</div>)', t, flags=re.S)
print("panels2:", len(panels2))
i = t.find("tli-content")
with open("tmp_csm2.txt", "w", encoding="utf-8") as f:
    f.write(t[i-200:i+2000])
