# -*- coding: utf-8 -*-
"""Consolidate roster + profiles into the canonical data/faculty.json."""
import re, os, json, html, unicodedata
from datetime import datetime, timezone

BASE = os.path.dirname(__file__)
QDIR = os.path.join(BASE, "data")
os.makedirs(QDIR, exist_ok=True)


def slug(s):
    """Slug that preserves CJK by using per-char code points when ASCII is empty."""
    s2 = unicodedata.normalize("NFKD", s)
    s2 = re.sub(r"[^A-Za-z0-9]+", "-", s2).strip("-").lower()
    if s2:
        return s2
    return "-".join("u%04x" % ord(ch) for ch in s if not ch.isspace()) or "x"


roster = json.load(open(os.path.join(BASE, "roster_raw.json"), encoding="utf-8"))
profiles = json.load(open(os.path.join(BASE, "profiles_final.json"), encoding="utf-8"))
manifest = json.load(open(os.path.join(BASE, "profile_manifest.json"), encoding="utf-8"))

SCHOOL = "清华大学"
DEPTS = {"phys": "物理系", "ep": "工程物理系", "ias": "高等研究院"}


def find_profile(name, site):
    for k, v in profiles.items():
        if v["name"] == name and v["site"] == site:
            return v
    return None


VENUE_PAT = re.compile(
    r'\b(Nature(?:\s+\w+)?|Science|Physical Review(?:\s+[A-Z])?|Phys\.?\s*Rev\.?(?:\s+[A-Z])?|'
    r'Phys\.?\s*Rev\.?\s*Lett\.?|Applied Physics Letters|J\.?\s*Am\.?\s*Chem\.?\s*Soc\.?|'
    r'Advanced Materials|Adv\.?\s*Mater\.?|Nano Letters|Nano Lett\.?|Nature Physics|'
    r'Nature Communications|Nature Materials|Nat\.?\s*Phys\.?|Nat\.?\s*Commun\.?|'
    r'PNAS|Proc\.?\s*Natl\.?\s*Acad\.?\s*Sci\.?|Cell|eLife|Angew\.?\s*Chem\.?|'
    r'Phys\.?\s*Lett\.?|Nucl\.?\s*Instrum\.?\s*Meth\.?|IEEE\s+Trans\.?|'
    r'Review of Scientific Instruments|J\.?\s*Appl\.?\s*Phys\.?|Optics Letters|'
    r'Opt\.?\s*Lett\.?|New Journal of Physics|Sci\.?\s*Adv\.?|Phys\.?\s*Rev\.?\s*B|'
    r'Phys\.?\s*Rev\.?\s*D|Phys\.?\s*Rev\.?\s*E|Phys\.?\s*Rev\.?\s*X|'
    r'J\.?\s*High Energy Phys\.?|JHEP|Astrophys\.?\s*J\.?|Astron\.?\s*J\.?|'
    r'Astron\.?\s*Astrophys\.?|Mon\.?\s*Not\.?\s*R\.?\s*Astron\.?\s*Soc\.?)',
    re.I)


def parse_pubs(raw, maxn=5):
    if not raw:
        return []
    parts = re.split(r'(?:^|\n)\s*\d{1,2}[\.\、\)]\s*', "\n" + raw)
    items = []
    for p in parts:
        p = re.sub(r"\s+", " ", p).strip()
        if len(p) < 15:
            continue
        year = None
        yfull = re.search(r'\b((?:19|20)\d{2})\b', p)
        if yfull:
            year = int(yfull.group(1))
        venue = ""
        vm = VENUE_PAT.search(p)
        if vm:
            venue = vm.group(1).strip()
        items.append({"title": p[:260], "venue": venue, "year": year})
        if len(items) >= maxn:
            break
    return items


def clean_summary(pf, limit=260):
    """Prefer the department's own 研究概况 text, then research text, then meta."""
    if not pf:
        return ""
    src = (pf.get("summary_raw") or "").strip()
    if len(src) < 25:
        src = (pf.get("research") or "").strip()
    if len(src) < 25:
        src = (pf.get("meta") or "").strip()
    src = re.sub(r"\s+", " ", src).strip()
    if not src:
        return ""
    return src[:limit].rstrip() + ("…" if len(src) > limit else "")


def short_directions(text, maxn=4):
    """Derive short research-direction chips from a free-text 研究领域 block."""
    if not text:
        return []
    # split on Chinese/English punctuation and list markers
    parts = re.split(r'[，,；;。\n]|、|（\d）|\(\d\)|\d\.', text)
    cand = []
    for p in parts:
        p = p.strip(" 　:：.-·")
        # keep concise phrases
        if 3 <= len(p) <= 22 and re.search(r'[\u4e00-\u9fff]', p):
            cand.append(p)
    # dedupe preserving order
    seen = set()
    out = []
    for c in cand:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out[:maxn]


records = []
seen = set()

# --- PHYSICS ---
phys_dirs = {}
for cat, people in roster["phys_byfield"].items():
    for p in people:
        phys_dirs.setdefault(p["name"], set()).add(cat)
sup_dirs = {}
for d, people in roster["phys_supervisors"].items():
    for p in people:
        sup_dirs.setdefault(p["name"], set()).add(d)

for cat, people in roster["phys_byfield"].items():
    for p in people:
        nm = p["name"]
        if nm in seen:
            continue
        seen.add(nm)
        pf = find_profile(nm, "phys")
        dirs = sorted(phys_dirs.get(nm, set()))
        allsup = sorted(sup_dirs.get(nm, set()))
        focus = [s for s in allsup if s not in dirs]
        title = ""
        if pf and pf.get("name_title"):
            title = pf["name_title"].replace(nm, "").strip(" ，,")
        records.append({
            "id": "tsinghua-phys-" + slug(nm),
            "name": nm,
            "name_local": nm,
            "school": SCHOOL,
            "department": "物理系",
            "title": title,
            "subject": "物理学",
            "research_directions": dirs,
            "focus_areas": focus[:5],
            "summary": clean_summary(pf),
            "publications": parse_pubs(pf.get("publications_raw") if pf else ""),
            "homepage": (pf.get("homepage") if pf else "") or "",
            "profile_url": "https://www.phys.tsinghua.edu.cn" + p["url"].replace("../../", "/"),
            "email": (pf.get("email") if pf else "") or "",
            "sources": ["https://www.phys.tsinghua.edu.cn/ry/jsfc/azyfl.htm"],
            "confidence": "fine" if (pf and (pf.get("research") or pf.get("email"))) else "coarse",
            "verified": True,
        })

# --- EP ---
for p in roster["ep"]:
    nm = p["name"]
    key = "ep-" + slug(nm + "_" + p["url"].split("/")[-1])
    if key in seen:
        continue
    seen.add(key)
    pf = find_profile(nm, "ep")
    url = p["url"].replace("../../../", "/").replace("../../", "/")
    dirs = short_directions(pf.get("research") if pf else "")
    records.append({
        "id": "tsinghua-ep-" + slug(nm) + "-" + p["url"].split("/")[-1].replace(".htm", ""),
        "name": nm,
        "name_local": nm,
        "school": SCHOOL,
        "department": "工程物理系",
        "title": p.get("jobtitle", "") or p.get("rank", ""),
        "subject": "核科学与技术 / 物理学",
        "research_directions": dirs,
        "focus_areas": [],
        "summary": clean_summary(pf),
        "publications": parse_pubs(pf.get("publications_raw") if pf else ""),
        "homepage": "",
        "profile_url": "https://www.ep.tsinghua.edu.cn" + url,
        "email": (pf.get("email") if pf else "") or "",
        "sources": ["https://www.ep.tsinghua.edu.cn/szdw/jsdw.htm"],
        "confidence": "fine" if (pf and (pf.get("research") or pf.get("email"))) else "coarse",
        "verified": True,
    })

# --- IAS ---
for p in roster["ias"]:
    nm = p["name"]
    key = "ias-" + slug(nm)
    if key in seen:
        continue
    seen.add(key)
    pf = find_profile(nm, "ias")
    url = p["url"].replace("../", "/")
    field = p.get("field", "") or ""
    records.append({
        "id": "tsinghua-ias-" + slug(nm),
        "name": nm,
        "name_local": nm,
        "school": SCHOOL,
        "department": "高等研究院",
        "title": p.get("title", ""),
        "subject": field or "物理学",
        "research_directions": [field] if field else [],
        "focus_areas": [],
        "summary": clean_summary(pf),
        "publications": parse_pubs(pf.get("publications_raw") if pf else ""),
        "homepage": (pf.get("homepage") if pf else "") or "",
        "profile_url": ("https://www.ias.tsinghua.edu.cn" + url) if url.startswith("/") else p["url"],
        "email": p.get("email") or (pf.get("email") if pf else "") or "",
        "sources": ["https://www.ias.tsinghua.edu.cn/yjry/jy.htm"],
        "confidence": "fine",
        "verified": True,
    })

query = {"schools": [SCHOOL], "departments": ["物理系", "工程物理系", "高等研究院"], "topics": ["物理学"]}
data = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "query": query,
    "professors": records,
}
json.dump(data, open(os.path.join(QDIR, "faculty.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("records:", len(records))
from collections import Counter
print(Counter(r["department"] for r in records))
print("with research:", sum(1 for r in records if r["research_directions"]))
print("with summary:", sum(1 for r in records if r["summary"]))
print("with email:", sum(1 for r in records if r["email"]))
print("with pubs:", sum(1 for r in records if r["publications"]))
print("fine:", sum(1 for r in records if r["confidence"] == "fine"))
