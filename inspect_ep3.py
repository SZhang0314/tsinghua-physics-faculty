# -*- coding: utf-8 -*-
import re, json, os
PROF = "data/raw/profiles"
man = json.load(open("profile_manifest.json", encoding="utf-8"))
rec = [r for r in man if r["site"] == "ep" and r.get("file")][0]
c = open(os.path.join(PROF, rec["file"]), encoding="utf-8", errors="ignore").read()
print("KEY", rec["key"], "len", len(c))
# find the tab content divs
for m in re.finditer(r'<div[^>]*id="([^"]*)"[^>]*>', c):
    pass
# dump all div ids
ids = re.findall(r'id="([^"]+)"', c)
with open("tmp_ep_ids.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(ids))
# find body content after header
i = c.find("vsb_content")
with open("tmp_ep_full.txt", "w", encoding="utf-8") as f:
    f.write(c[i:i+6000])
