# -*- coding: utf-8 -*-
import re, os, time, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "data", "raw")

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    data = urllib.request.urlopen(req, timeout=30).read()
    head = data[:2000].decode("ascii", "ignore").lower()
    if "charset=gb" in head:
        return data.decode("gb18030", "ignore")
    return data.decode("utf-8", "ignore")

base = "https://www.ep.tsinghua.edu.cn/szdw/jsdw"
pages = {
    "ep-senior": base + "/zc/zgj1.htm",
    "ep-senior-p1": base + "/zc/zgj1/1.htm",
    "ep-senior-p2": base + "/zc/zgj1/2.htm",
    "ep-senior-p3": base + "/zc/zgj1/3.htm",
    "ep-assoc": base + "/zc/fgj1.htm",
    "ep-assoc-p1": base + "/zc/fgj1/1.htm",
    "ep-assoc-p2": base + "/zc/fgj1/2.htm",
    "ep-assoc-p3": base + "/zc/fgj1/3.htm",
    "ep-mid": base + "/zc/zj1.htm",
}
for n, u in pages.items():
    try:
        t = fetch(u)
        with open(os.path.join(OUT, n + ".html"), "w", encoding="utf-8") as f:
            f.write(t)
        print("OK  %-16s len=%d blocks=%d" % (n, len(t), t.count('class="teacher-name"')))
    except Exception as e:
        print("ERR %-16s %s" % (n, e))
    time.sleep(0.4)
