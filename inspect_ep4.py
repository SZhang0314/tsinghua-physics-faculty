# -*- coding: utf-8 -*-
import re, os
c = open("data/raw/profiles/ep-chengcheng.html", encoding="utf-8", errors="ignore").read() if os.path.exists("data/raw/profiles/ep-chengcheng.html") else None
# find the ep chengcheng file by content (name 程诚)
import glob
target = None
for fp in glob.glob("data/raw/profiles/ep-*.html"):
    t = open(fp, encoding="utf-8", errors="ignore").read()
    if "程诚" in t and "4274" in t:
        target = fp
        break
print("target", target)
if target:
    t = open(target, encoding="utf-8", errors="ignore").read()
    # find main content - locate 研究方向 or 个人简介
    for kw in ["研究方向", "个人简介", "研究领域", "工作经历", "学习经历"]:
        i = t.find(kw)
        print(kw, i)
    i = t.find("vsb_content")
    if i < 0:
        i = t.find("content")
    with open("tmp_ep_cheng.txt", "w", encoding="utf-8") as f:
        f.write(t[i:i+7000])
