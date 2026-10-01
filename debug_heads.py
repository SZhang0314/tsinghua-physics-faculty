# -*- coding: utf-8 -*-
import re, json, os, collections
PROF = "data/raw/profiles"
man = json.load(open("profile_manifest.json", encoding="utf-8"))

def to_text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()

heads_counter = collections.Counter()
per_head = collections.Counter()
for rec in man:
    if not rec.get("file"):
        continue
    c = open(os.path.join(PROF, rec["file"]), encoding="utf-8", errors="ignore").read()
    hs = re.findall(r'<div class="xq-title[^"]*"[^>]*>\s*(.*?)\s*</div>', c, flags=re.S)
    per_head[rec["site"]] += len(hs)
    for h in hs:
        t = to_text(h).strip()[:20]
        if t:
            heads_counter[t] += 1
# dump
with open("tmp_heads.json", "w", encoding="utf-8") as f:
    json.dump({"headings": heads_counter.most_common(60), "per_site": per_head}, f, ensure_ascii=False, indent=1)
print("done", dict(per_head))
