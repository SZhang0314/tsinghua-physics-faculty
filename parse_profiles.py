# -*- coding: utf-8 -*-
"""Parse scraped profile pages into structured records and build faculty.json."""
import re, os, json

BASE = os.path.dirname(__file__)
RAW = os.path.join(BASE, "data", "raw")
PROF = os.path.join(RAW, "profiles")

def read(p):
    with open(p, encoding="utf-8", errors="ignore") as f:
        return f.read()

def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#34;", '"').replace("&gt;", ">").replace("&lt;", "<")
    return re.sub(r"\s+", " ", s).strip()

def meta_desc(c):
    m = re.search(r'<meta name="description" content="([^"]*)"', c)
    return clean(m.group(1)) if m else ""

def parse_phys(c):
    """Physics dept profile: teacher-name (name+title), teacher-p (email/phone/addr), 研究领域."""
    out = {}
    m = re.search(r'<div class="teacher-name">\s*(.*?)</div>', c, flags=re.S)
    if m:
        nt = clean(m.group(1))
        out["name_title"] = nt
    # email
    em = re.search(r'邮箱[:：]\s*<a[^>]*>(.*?)</a>', c, flags=re.S)
    if not em:
        em = re.search(r'邮箱[:：]\s*([^\s<]+@[^\s<]+)', c)
    if em:
        out["email"] = clean(em.group(1)).replace("(AT)", "@").replace("(at)", "@").replace("（AT）", "@")
    # research area: text after 研究领域
    ra = re.search(r'研究领域(.*?)(?:招生|代表性|论文|发表|$)', c, flags=re.S)
    if ra:
        txt = clean(ra.group(1))
        out["research"] = txt[:1200]
    return out

def parse_ep(c):
    out = {}
    # EP pages vary; find bio + research
    m = re.search(r'class="xq[^"]*"[^>]*>(.*?)</div>', c, flags=re.S)
    out["meta"] = meta_desc(c)
    # email
    em = re.search(r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})', c)
    if em:
        out["email"] = em.group(1)
    for kw in ["研究方向", "研究领域", "科研方向", "主要研究"]:
        m2 = re.search(kw + r'[：:]?\s*(.*?)(?:代表|论文|招生|教育|工作|$)', c, flags=re.S)
        if m2:
            out["research"] = clean(m2.group(1))[:1200]
            break
    return out

def parse_ias(c):
    out = {}
    out["meta"] = meta_desc(c)
    em = re.search(r'([A-Za-z0-9._%+-]+(?:@|\(at\)|\(AT\))[A-Za-z0-9.-]+)', c)
    if em:
        out["email"] = em.group(1).replace("(at)", "@").replace("(AT)", "@")
    # personal homepage
    hp = re.search(r'个人主页[：:]\s*(?:<[^>]+>)*\s*(https?://[^\s<"]+)', c)
    if not hp:
        hp = re.search(r'个人主页[：:]\s*(http[^\s<"]+)', c)
    if hp:
        out["homepage"] = hp.group(1)
    # research from meta description usually has bio
    return out

def parse(key, site, c):
    if site == "phys":
        return parse_phys(c)
    if site == "ep":
        return parse_ep(c)
    return parse_ias(c)

if __name__ == "__main__":
    man = json.load(open(os.path.join(BASE, "profile_manifest.json"), encoding="utf-8"))
    parsed = {}
    for rec in man:
        if not rec.get("file"):
            continue
        c = read(os.path.join(PROF, rec["file"]))
        parsed[rec["key"]] = parse(rec["key"], rec["site"], c)
    with open(os.path.join(BASE, "profiles_parsed.json"), "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=1)
    print("parsed:", len(parsed))
    sample = [k for k in parsed][:3]
    for k in sample:
        print(k, "->", json.dumps(parsed[k], ensure_ascii=False)[:300])
