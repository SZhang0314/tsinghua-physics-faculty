# -*- coding: utf-8 -*-
import os, urllib.request, time

OUT = os.path.join(os.path.dirname(__file__), "data", "raw", "profiles")
os.makedirs(OUT, exist_ok=True)

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    data = urllib.request.urlopen(req, timeout=30).read()
    head = data[:2000].decode("ascii", "ignore").lower()
    if "charset=gb" in head:
        return data.decode("gb18030", "ignore")
    return data.decode("utf-8", "ignore")

samples = {
    "phys-hesong": "https://www.phys.tsinghua.edu.cn/info/1102/4530.htm",   # 段文晖
    "ep-chengcheng": "https://www.ep.tsinghua.edu.cn/info/1236/4274.htm",    # 程诚
    "ias-baixuening": "https://www.ias.tsinghua.edu.cn/info/1016/1234.htm",  # 白雪宁
}
for n, u in samples.items():
    try:
        t = fetch(u)
        with open(os.path.join(OUT, n + ".html"), "w", encoding="utf-8") as f:
            f.write(t)
        print("OK", n, len(t))
    except Exception as e:
        print("ERR", n, e)
    time.sleep(0.4)
