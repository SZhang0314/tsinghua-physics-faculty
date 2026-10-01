# -*- coding: utf-8 -*-
import re, json, time, os, urllib.request, urllib.parse

OUT = os.path.join(os.path.dirname(__file__), "data", "raw")
os.makedirs(OUT, exist_ok=True)

def fetch(url, name=None):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    data = urllib.request.urlopen(req, timeout=30).read()
    head = data[:2000].decode("ascii", "ignore").lower()
    if "charset=gb" in head or "charset=\"gb" in head:
        text = data.decode("gb18030", "ignore")
    else:
        text = data.decode("utf-8", "ignore")
    if name:
        with open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8") as f:
            f.write(text)
    return text

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip()

if __name__ == "__main__":
    base = {
        "phys": "https://www.phys.tsinghua.edu.cn",
        "ep": "https://www.ep.tsinghua.edu.cn",
        "ias": "https://www.ias.tsinghua.edu.cn",
    }
    pages = {
        "phys-pinyin": base["phys"] + "/ry/jsfc/apysx.htm",
        "phys-byfield": base["phys"] + "/ry/jsfc/azyfl.htm",
        "phys-supervisors": base["phys"] + "/yjs1/dsjyjfx.htm",
        "ias-faculty": base["ias"] + "/yjry/jy.htm",
        "ias-cond-theory": base["ias"] + "/yjly/njtwl.htm",
        "ias-amr": base["ias"] + "/yjly/lyzwl.htm",
        "ias-comp-phys": base["ias"] + "/yjly/jsjkx.htm",
        "ias-biophys": base["ias"] + "/yjly/llswwl.htm",
        "ias-math": base["ias"] + "/yjly/sx.htm",
        "ias-astro": base["ias"] + "/yjly/ttwl.htm",
        "ep-senior": base["ep"] + "/szdw/jsdw/zc/zgj1.htm",
        "ep-assoc": base["ep"] + "/szdw/jsdw/zc/fgj1.htm",
        "ep-mid": base["ep"] + "/szdw/jsdw/zc/zj1.htm",
    }
    for n, u in pages.items():
        try:
            t = fetch(u, n)
            print("OK  %-18s len=%d" % (n, len(t)))
        except Exception as e:
            print("ERR %-18s %s" % (n, e))
        time.sleep(0.5)
