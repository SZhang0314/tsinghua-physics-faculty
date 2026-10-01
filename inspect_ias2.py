# -*- coding: utf-8 -*-
import re
c = open("data/raw/profiles/ias-baixuening.html", encoding="utf-8").read()
i = c.find("白雪宁")
seg = c[i-200:i+4000]
with open("tmp_ias2.txt", "w", encoding="utf-8") as f:
    f.write(seg)
print("idx", i, "len", len(c))
# save the main article region
j = c.find("article")
print(c.count("vsb_content"), c.count("研究领域"), c.count("研究方向"))
