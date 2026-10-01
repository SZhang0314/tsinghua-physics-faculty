# -*- coding: utf-8 -*-
import re
c = open("data/raw/profiles/phys-曹远胜.html", encoding="utf-8", errors="ignore").read()
# find all xq-title headings
for m in re.finditer(r'<div class="xq-title[^"]*"[^>]*>\s*(.*?)\s*</div>', c, flags=re.S):
    print("HEADING:", re.sub(r"\s+"," ",m.group(1)).strip(), "@", m.start())
# find body container
i = c.find('class="teach-top')
print("teach-top idx", i)
j = c.find('<div class="jl-txt')
print("jl-txt idx", j)
with open("tmp_cys2.txt","w",encoding="utf-8") as f:
    f.write(c[j:j+2500] if j>0 else c[i:i+2500])
