# -*- coding: utf-8 -*-
"""Scrape all faculty profile pages listed in roster_raw.json."""
import re, os, json, time, urllib.request, urllib.parse

BASE = os.path.dirname(__file__)
RAW = os.path.join(BASE, "data", "raw")
PROF = os.path.join(RAW, "profiles")
os.makedirs(PROF, exist_ok=True)

SITES = {
    "phys": "https://www.phys.tsinghua.edu.cn",
    "ep": "https://www.ep.tsinghua.edu.cn",
    "ias": "https://www.ias.tsinghua.edu.cn",
}

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    data = urllib.request.urlopen(req, timeout=30).read()
    head = data[:2000].decode("ascii", "ignore").lower()
    if "charset=gb" in head:
        return data.decode("gb18030", "ignore")
    return data.decode("utf-8", "ignore")

def abs_url(site, href):
    if not href:
        return ""
    if href.startswith("http"):
        return href
    return urllib.parse.urljoin(SITES[site] + "/", href)

def slug(site, name):
    return site + "-" + re.sub(r'\W+', '_', name)

def main():
    roster = json.load(open(os.path.join(BASE, "roster_raw.json"), encoding="utf-8"))
    jobs = []  # (key, url, site, name)
    for cat, people in roster["phys_byfield"].items():
        for p in people:
            jobs.append((slug("phys", p["name"]), abs_url("phys", p["url"]), "phys", p["name"]))
    for p in roster["ep"]:
        jobs.append((slug("ep", p["name"] + "_" + p["url"].split("/")[-1]), abs_url("ep", p["url"]), "ep", p["name"]))
    for p in roster["ias"]:
        if p["url"]:
            jobs.append((slug("ias", p["name"]), abs_url("ias", p["url"]), "ias", p["name"]))

    # dedupe by key
    seen = set()
    uniq = []
    for j in jobs:
        if j[0] not in seen:
            seen.add(j[0])
            uniq.append(j)

    print("total profile jobs:", len(uniq))
    manifest = []
    for i, (key, url, site, name) in enumerate(uniq):
        fp = os.path.join(PROF, key + ".html")
        if os.path.exists(fp) and os.path.getsize(fp) > 500:
            manifest.append({"key": key, "url": url, "site": site, "name": name, "file": key + ".html"})
            continue
        try:
            t = fetch(url)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(t)
            manifest.append({"key": key, "url": url, "site": site, "name": name, "file": key + ".html"})
            if i % 20 == 0:
                print("  [%d/%d] %s" % (i, len(uniq), name))
        except Exception as e:
            manifest.append({"key": key, "url": url, "site": site, "name": name, "file": "", "error": str(e)})
            print("  ERR", name, e)
        time.sleep(0.35)
    with open(os.path.join(BASE, "profile_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("done. manifest:", len(manifest))

if __name__ == "__main__":
    main()
