# -*- coding: utf-8 -*-
import json
d = json.load(open("data/faculty.json", encoding="utf-8"))
eps = [p for p in d["professors"] if p["department"] == "工程物理系"]
out = []
for p in eps[:6]:
    out.append({"name": p["name"], "title": p["title"], "summary": p["summary"][:150],
                "email": p["email"], "pubs": len(p["publications"])})
json.dump(out, open("qc_ep.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("EP count", len(eps), "with summary", sum(1 for p in eps if p["summary"]),
      "with pubs", sum(1 for p in eps if p["publications"]))
