# -*- coding: utf-8 -*-
import json
d = json.load(open("profiles_final.json", encoding="utf-8"))
eps = [v for k, v in d.items() if v["site"] == "ep"]
miss = [{"name": v["name"], "url": v["url"], "H": v["_headings"]} for v in eps if not v["research"]]
json.dump(miss, open("qc_ep_missing2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# show a sample
out = []
for v in eps[:4]:
    out.append({"name": v["name"], "research": v["research"][:200], "summary": v.get("summary_raw","")[:120],
                "email": v["email"], "pubs_h": v["publications_raw"][:120], "H": v["_headings"]})
json.dump(out, open("qc_ep_sample.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done")
