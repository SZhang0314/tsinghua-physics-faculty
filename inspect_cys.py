# -*- coding: utf-8 -*-
import re
c = open("data/raw/profiles/phys-曹远胜.html", encoding="utf-8", errors="ignore").read()
i = c.find("研究领域")
print("idx", i)
with open("tmp_cys.txt", "w", encoding="utf-8") as f:
    f.write(c[i-200:i+2500] if i > 0 else c[:2500])
