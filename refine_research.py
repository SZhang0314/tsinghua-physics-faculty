# -*- coding: utf-8 -*-
"""Refine research extraction for physics profiles: capture text right after 研究领域 heading."""
import re, json, os
PROF = "data/raw/profiles"
man = json.load(open("profile_manifest.json", encoding="utf-8"))

def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#34;", '"')
    return re.sub(r"\s+", " ", s).strip()

results = {}
for rec in man:
    if rec["site"] != "phys" or not rec.get("file"):
        continue
    c = open(os.path.join(PROF, rec["file"]), encoding="utf-8", errors="ignore").read()
    # locate the 研究领域 heading div
    m = re.search(r'研究领域</div>(.*?)(?:<div class="xq-title|招生|代表性|发表论文|学术成果|$)', c, flags=re.S)
    txt = ""
    if m:
        txt = clean(m.group(1))
    results[rec["key"]] = txt[:600]

# print a few to judge
import itertools
for k, v in itertools.islice(results.items(), 8):
    print("----", k)
    print(v[:300])
with open("phys_research_raw.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
