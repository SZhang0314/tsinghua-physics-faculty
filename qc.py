# -*- coding: utf-8 -*-
import json
d = json.load(open("profiles_final.json", encoding="utf-8"))
out = {}
for k in ["phys-陈难先", "phys-薛其坤", "phys-段文晖", "ep-程诚", "ias-白雪宁", "phys-曹远胜"]:
    if k in d:
        v = d[k]
        out[k] = {
            "site": v["site"],
            "email": v["email"],
            "homepage": v.get("homepage", ""),
            "headings": v["_headings"],
            "research": (v["research"] or "")[:500],
            "pubs": (v["publications_raw"] or "")[:300],
        }
json.dump(out, open("qc_show.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
