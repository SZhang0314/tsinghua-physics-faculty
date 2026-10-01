# -*- coding: utf-8 -*-
"""Build consolidated roster from all parsed sources -> data/roster.json"""
import re, json, os

RAW = os.path.join(os.path.dirname(__file__), "data", "raw")
BASE = os.path.dirname(__file__)

def read(name):
    with open(os.path.join(RAW, name + ".html"), encoding="utf-8") as f:
        return f.read()

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#34;", '"')
    return re.sub(r"\s+", " ", s).strip()

def nn(s):
    return re.sub(r"\s+", "", clean(s))

# --- Physics by field ---
def phys_byfield():
    c = read("phys-byfield")
    out = {}
    parts = re.split(r'<p class="lmmc_index_l"[^>]*>(.*?)</p>', c, flags=re.S)
    for i in range(1, len(parts) - 1, 2):
        cat = clean(parts[i])
        block = parts[i + 1]
        people = []
        for m in re.finditer(r'<a href="([^"]+)"[^>]*title="([^"]*)"[^>]*>', block):
            nm = nn(m.group(2))
            if nm and "info/" in m.group(1):
                people.append({"name": nm, "url": m.group(1).strip()})
        if people:
            out[cat] = people
    return out

# --- Physics supervisors (research direction) ---
def phys_supervisors():
    c = read("phys-supervisors")
    out = {}
    rows = re.findall(r'<strong>(.*?)</strong></p></td>(.*?)</td>', c, flags=re.S)
    for d, block in rows:
        d = clean(d).rstrip("：: ")
        people = []
        for lm in re.finditer(r'<a href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.S):
            nm = nn(lm.group(2))
            if nm:
                people.append({"name": nm, "url": lm.group(1).strip()})
        if d and people:
            out[d] = people
    return out

# --- EP roster (all rank pages) ---
def ep_roster():
    files = [
        ("ep-senior", "正高级"), ("ep-senior-p1", "正高级"),
        ("ep-senior-p2", "正高级"), ("ep-senior-p3", "正高级"),
        ("ep-assoc", "副高级"), ("ep-assoc-p1", "副高级"),
        ("ep-assoc-p2", "副高级"), ("ep-assoc-p3", "副高级"),
        ("ep-mid", "中级"),
    ]
    res = []
    for fname, rank in files:
        c = read(fname)
        for b in re.split(r'<div class="teacher-name">', c)[1:]:
            nm_m = re.search(r'<a href="([^"]+)">(.*?)</a>', b, flags=re.S)
            if not nm_m:
                continue
            href = nm_m.group(1).strip()
            nm = nn(nm_m.group(2))
            job = ""
            jm = re.search(r'职称[：:]\s*([^<）)\s]+)', b, flags=re.S)
            if jm:
                job = jm.group(1).strip()
            if nm:
                res.append({"name": nm, "url": href, "rank": rank, "jobtitle": job})
    # dedupe by name+url
    seen = {}
    for r in res:
        k = (r["name"], r["url"])
        if k not in seen:
            seen[k] = r
    return list(seen.values())

# --- IAS roster ---
def ias_roster():
    c = read("ias-faculty")
    people = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", c, flags=re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)
        if len(tds) < 4:
            continue
        name_td = tds[0]
        if "姓名" in clean(name_td):
            continue
        a = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>', name_td, flags=re.S)
        nm = nn(a.group(2)) if a else nn(name_td)
        href = a.group(1).strip() if a else ""
        if not nm:
            continue
        people.append({
            "name": nm,
            "url": href,
            "title": clean(tds[1]),
            "field": clean(tds[2]),
            "email": clean(tds[3]).replace("(AT)", "@").replace("(at)", "@"),
        })
    return people

if __name__ == "__main__":
    data = {
        "phys_byfield": phys_byfield(),
        "phys_supervisors": phys_supervisors(),
        "ep": ep_roster(),
        "ias": ias_roster(),
    }
    with open(os.path.join(BASE, "roster_raw.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("phys_byfield cats:", {k: len(v) for k, v in data["phys_byfield"].items()})
    print("phys_supervisors dirs:", len(data["phys_supervisors"]),
          sum(len(v) for v in data["phys_supervisors"].values()))
    print("ep:", len(data["ep"]))
    print("ias:", len(data["ias"]))
