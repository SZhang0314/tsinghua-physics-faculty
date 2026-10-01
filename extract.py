# -*- coding: utf-8 -*-
"""Extract faculty rosters from Tsinghua physics-related departments."""
import re, json, os

RAW = os.path.join(os.path.dirname(__file__), "data", "raw")

def read(name):
    with open(os.path.join(RAW, name + ".html"), encoding="utf-8") as f:
        return f.read()

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#34;", '"')
    return re.sub(r"\s+", " ", s).strip()

def name_norm(s):
    return re.sub(r"\s+", "", clean(s))

# ---------------- PHYSICS DEPARTMENT ----------------
def parse_phys_byfield():
    """Category -> list of (name, profile relative url)."""
    c = read("phys-byfield")
    out = {}
    # split by category headers <p class="lmmc_index_l" ...>CAT</p>
    parts = re.split(r'<p class="lmmc_index_l"[^>]*>(.*?)</p>', c, flags=re.S)
    # parts[0] preamble, then alternating cat, block
    for i in range(1, len(parts) - 1, 2):
        cat = clean(parts[i])
        block = parts[i + 1]
        people = []
        for m in re.finditer(r'<a href="([^"]+)"[^>]*title="([^"]*)"[^>]*>', block):
            href = m.group(1).strip()
            nm = name_norm(m.group(2))
            if nm and ("info/" in href or "http" in href):
                people.append({"name": nm, "url": href})
        if people:
            out[cat] = people
    return out

def parse_phys_pinyin():
    c = read("phys-pinyin")
    people = []
    for m in re.finditer(r'<a href="([^"]+)"[^>]*title="([^"]*)"[^>]*>', c):
        href = m.group(1).strip()
        nm = name_norm(m.group(2))
        if nm and ("info/" in href):
            people.append({"name": nm, "url": href})
    return people

def parse_phys_supervisors():
    """Research direction -> list of (name, profile url)."""
    c = read("phys-supervisors")
    out = {}
    for m in re.finditer(r'<strong>(.*?)：?</strong>', c, flags=re.S):
        pass
    # Each row: <strong>DIRECTION：</strong></p></td> <td ...> ... links ... </p></td>
    rows = re.findall(r'<strong>(.*?)</strong></p></td>(.*?)</td>', c, flags=re.S)
    for direction, block in rows:
        d = clean(direction).rstrip("：: ")
        people = []
        for lm in re.finditer(r'<a href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.S):
            nm = name_norm(lm.group(2))
            if nm:
                people.append({"name": nm, "url": lm.group(1).strip()})
        if d and people:
            out[d] = people
    return out

# ---------------- ENGINEERING PHYSICS ----------------
def parse_ep_rank():
    """Roster from EP rank pages."""
    result = []
    for fname, title in [("ep-senior", "正高级"), ("ep-assoc", "副高级"), ("ep-mid", "中级")]:
        c = read(fname)
        # teacher-name divs and optional teacher-p with 职称
        blocks = re.split(r'<div class="teacher-name">', c)
        for b in blocks[1:]:
            nm_m = re.search(r'<a href="([^"]+)">(.*?)</a>', b, flags=re.S)
            if not nm_m:
                continue
            href = nm_m.group(1).strip()
            nm = name_norm(nm_m.group(2))
            job = ""
            jm = re.search(r'职称[：:]\s*([^<）)\s]+)', b, flags=re.S)
            if jm:
                job = jm.group(1).strip()
            if nm:
                result.append({"name": nm, "url": href, "rank": title, "jobtitle": job})
    return result

# ---------------- INSTITUTE FOR ADVANCED STUDY ----------------
def parse_ias():
    c = read("ias-faculty")
    people = []
    # rows of the table: find <tr> ... </tr>, each with 4 tds
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", c, flags=re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)
        if len(tds) < 4:
            continue
        name_td = tds[0]
        if "姓名" in clean(name_td):
            continue
        a = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>', name_td, flags=re.S)
        nm = name_norm(a.group(2)) if a else name_norm(name_td)
        href = a.group(1).strip() if a else ""
        title = clean(tds[1])
        field = clean(tds[2])
        email = clean(tds[3]).replace("(AT)", "@").replace("(at)", "@").replace("（AT）", "@")
        if nm:
            people.append({"name": nm, "url": href, "title": title, "field": field, "email": email})
    return people

if __name__ == "__main__":
    data = {
        "phys_byfield": parse_phys_byfield(),
        "phys_pinyin_count": len(parse_phys_pinyin()),
        "phys_supervisors": parse_phys_supervisors(),
        "ep": parse_ep_rank(),
        "ias": parse_ias(),
    }
    with open(os.path.join(os.path.dirname(__file__), "parsed.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("phys_byfield cats:", {k: len(v) for k, v in data["phys_byfield"].items()})
    print("phys_pinyin:", data["phys_pinyin_count"])
    print("phys_supervisors dirs:", {k: len(v) for k, v in data["phys_supervisors"].items()})
    print("ep total:", len(data["ep"]))
    print("ias total:", len(data["ias"]))
