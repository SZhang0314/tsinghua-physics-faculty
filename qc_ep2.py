# -*- coding: utf-8 -*-
import json
d = json.load(open("profiles_final.json", encoding="utf-8"))
eps = [v for k, v in d.items() if v["site"] == "ep"]
print("EP total", len(eps))
print("  research", sum(1 for v in eps if v["research"]))
print("  summary_raw", sum(1 for v in eps if v.get("summary_raw")))
print("  pubs", sum(1 for v in eps if v["publications_raw"]))
print("  email", sum(1 for v in eps if v["email"]))
print("  headings present", sum(1 for v in eps if v["_headings"]))
# why missing research
missing = [v["name"] + " " + v["url"] + " H=" + str(v["_headings"][:4]) for v in eps if not v["research"]]
json.dump(missing[:20], open("qc_ep_missing.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("missing research:", len(missing))
