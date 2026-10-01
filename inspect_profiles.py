# -*- coding: utf-8 -*-
import re
for n in ["phys-hesong", "ep-chengcheng", "ias-baixuening"]:
    c = open("data/raw/profiles/%s.html" % n, encoding="utf-8").read()
    i = c.find('vsb_content')
    seg = c[i:i+3500] if i > 0 else c[:3500]
    with open("tmp_%s.txt" % n, "w", encoding="utf-8") as f:
        f.write(seg)
    print("wrote", n, "vsb_idx=", i)
