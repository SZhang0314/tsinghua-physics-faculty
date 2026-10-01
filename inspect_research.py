# -*- coding: utf-8 -*-
import re, json, os
PROF = "data/raw/profiles"
man = json.load(open("profile_manifest.json", encoding="utf-8"))
# Show the region around '研究领域' / '研究方向' for 3 phys, 2 ep, 2 ias
for rec in man:
    if rec["site"] not in ("phys", "ep"):
        continue
    c = open(os.path.join(PROF, rec["file"]), encoding="utf-8", errors="ignore").read()
    for kw in ["研究领域", "研究方向", "科研方向", "主要研究"]:
        i = c.find(kw)
        if i > 0:
            seg = c[i:i+700]
            txt = re.sub(r"<[^>]+>", " ", seg)
            txt = re.sub(r"\s+", " ", txt).strip()
            with open("tmp_r_%s.txt" % rec["key"][:24], "w", encoding="utf-8") as f:
                f.write(rec["name"] + " | " + kw + "\n" + txt)
            break
print("done")
