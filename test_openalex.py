# -*- coding: utf-8 -*-
import urllib.request, json, urllib.parse, time, os

BASE = os.path.dirname(__file__)

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": "faculty-directory/1.0 (mailto:research@example.com)"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))

def search_authors(name, per_page=6):
    q = urllib.parse.quote(name)
    url = "https://api.openalex.org/authors?search=%s&per_page=%d" % (q, per_page)
    try:
        return api(url).get("results", [])
    except Exception as e:
        return []

def inst_names(a):
    s = set()
    for i in (a.get("last_known_institutions") or []):
        s.add(i.get("display_name", ""))
    for af in (a.get("affiliations") or []):
        s.add((af.get("institution") or {}).get("display_name", ""))
    return s

if __name__ == "__main__":
    for nm in ["段文晖", "薛其坤", "白雪宁"]:
        print("==", nm)
        for a in search_authors(nm)[:4]:
            print("  ", a.get("display_name"), "works=", a.get("works_count"),
                  "cited=", a.get("cited_by_count"), "|", list(inst_names(a))[:3])
        time.sleep(0.3)
