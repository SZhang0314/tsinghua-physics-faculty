# -*- coding: utf-8 -*-
import re
c = open("data/raw/ep-senior.html", encoding="utf-8").read()
i = c.find('class="pages"')
seg = c[i:i+1500]
with open("tmp_ep.txt", "w", encoding="utf-8") as f:
    f.write(seg)
print("written", i)
