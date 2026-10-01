# -*- coding: utf-8 -*-
"""Robust, template-agnostic profile parser.

Works on cleaned plain text: split by known section headings, extract
research directions and publications.
"""
import re, os, json, html

PROF = "data/raw/profiles"

HEADINGS = [
    "个人简历", "简历", "教育背景", "学习经历", "工作经历", "教学",
    "研究领域", "研究方向", "科研方向", "研究兴趣", "主要研究",
    "奖励、荣誉和学术兼职", "奖励荣誉", "荣誉", "获奖",
    "主要论著", "主要论文", "代表性论文", "代表性文章", "代表论文",
    "学术成果", "发表论文", "论文", "著作", "科研项目", "承担项目",
    "现任学术兼职", "学术兼职", "联系方式", "招生", "个人主页",
]

def to_text(s):
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>|</div>|</tr>|</li>|</td>|</h\d>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\u00a0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()

def content_start(c):
    """Find where the person's content begins (skip nav)."""
    for marker in ['按专业分类', '按拼音顺序', 'teacher-name', 'teach-top']:
        i = c.find(marker)
        if i > 0:
            return i
    # IAS template: content after the last nav element '来访学者' or '学术交流'
    for marker in ['来访学者', '学术会议', '访学者', '人员招聘']:
        i = c.rfind(marker)
        if i > 0:
            return i
    return 0

def strip_ias_nav(txt, name):
    """Remove the repeated IAS nav block that precedes the real research text."""
    # nav repeats many short tokens; the real content starts after '来访学者'
    for marker in ["来访学者", "学术会议", "学术报告", "学术交流"]:
        i = txt.rfind(marker)
        if i > 0:
            return txt[i + len(marker):]
    return txt

def email_in(s):
    m = re.search(r'([A-Za-z0-9._%+\-]+)\s*(?:@|\(at\)|\(AT\)|（at）|（AT）)\s*([A-Za-z0-9.\-]+\.[A-Za-z]{2,})', s)
    return (m.group(1) + "@" + m.group(2)) if m else ""

def split_text_sections(txt):
    """Split cleaned text into sections keyed by canonical heading tokens found on their own line."""
    lines = txt.split("\n")
    sections = {}
    cur = "__pre__"
    buf = []
    def flush():
        if buf:
            sections.setdefault(cur, [])
            sections[cur].append("\n".join(buf))
    for ln in lines:
        stripped = re.sub(r"^[\d\.\、\s]+", "", ln).strip()
        hit = None
        for h in HEADINGS:
            if stripped == h or (stripped.startswith(h) and len(stripped) <= len(h) + 6):
                hit = h
                break
        if hit:
            flush()
            buf = []
            cur = hit
        else:
            buf.append(ln)
    flush()
    return {k: "\n".join(v).strip() for k, v in sections.items()}

def get_research(sections):
    for k in ["研究领域", "研究方向", "科研方向", "研究兴趣", "主要研究"]:
        if sections.get(k):
            return sections[k][:1600]
    return ""

def get_pubs(sections):
    for k in ["主要论著", "主要论文", "代表性论文", "代表性文章", "代表论文", "学术成果", "发表论文", "论文"]:
        if sections.get(k):
            return sections[k][:3000]
    return ""

def clean_pubs(txt):
    """Cut footer boilerplate."""
    if not txt:
        return ""
    cut = txt
    for marker in ["友情链接", "联系地址", "版权所有", "传真：010-6278", "Email: wlx@tsinghua"]:
        i = cut.find(marker)
        if i > 0:
            cut = cut[:i]
    return cut.strip()

def parse_ep_tabs(c):
    """EP profiles use right-column menu + tli-content panels."""
    out = {}
    md = re.search(r'<meta name="description" content="([^"]*)"', c)
    meta = html.unescape(md.group(1)) if md else ""
    out["meta"] = meta
    # menu items may contain newlines
    menu = re.findall(r'<div class="text">\s*(.*?)\s*</div>', c, flags=re.S)
    menu = [to_text(m).strip() for m in menu]
    panels = re.findall(
        r'<div class="tli-content([^"]*)">(.*?)(?=<div class="tli-content|</div>\s*</div>\s*</div>|</div>\s*<div style="clear)',
        c, flags=re.S)
    if len(panels) < 2:
        panels = re.findall(r'<div class="tli-content([^"]*)">(.*?)(?=<div class="tli-content|$)', c, flags=re.S)
    secs = {}
    # first map by menu order
    for i, (cls, pan) in enumerate(panels):
        name = menu[i] if i < len(menu) else ""
        if not name:
            name = semantic_ep(cls)
        secs[name] = to_text(pan).strip()
    out["_headings"] = list(secs.keys())
    out["research"] = secs.get("研究领域", "") or secs.get("研究方向", "")
    out["summary_raw"] = secs.get("研究概况", "")
    out["publications_raw"] = clean_pubs(secs.get("学术成果", ""))
    emails = re.findall(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}', c)
    personal = [e for e in emails if e.lower() != "gwbgs@mail.tsinghua.edu.cn"]
    out["email"] = personal[0] if personal else ""
    out["homepage"] = ""
    return out, secs, meta

SEM_EP = {
    "jy-background": "教育背景", "job-record": "工作经历",
    "teaching": "教学工作", "research-field": "研究领域",
    "research-overview": "研究概况", "academic-achievement": "学术成果",
    "academic-parttime": "学术兼职", "award-honor": "奖励荣誉",
}

def semantic_ep(cls):
    for k, v in SEM_EP.items():
        if k in cls:
            return v
    return ""

def parse_common(c):
    # EP tab template?
    if 'class="tli-content' in c and '<div class="text">' in c:
        return parse_ep_tabs(c)
    out = {}
    start = content_start(c)
    txt = to_text(c[start:])
    # also parse meta description as fallback
    md = re.search(r'<meta name="description" content="([^"]*)"', c)
    meta = html.unescape(md.group(1)) if md else ""
    out["email"] = email_in(txt) or email_in(meta)
    sections = split_text_sections(txt)
    research = get_research(sections)
    # For IAS, strip leading nav tokens
    if research:
        research = strip_ias_nav(research, "")
    out["research"] = research
    out["publications_raw"] = clean_pubs(get_pubs(sections))
    out["summary_raw"] = sections.get("研究概况", "")
    # homepage: take first URL token only
    hp = re.search(r'个人主页[：:混]*\s*(?:<[^>]+>)*\s*(https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+)', c)
    if not hp:
        hp = re.search(r'个人网页[：:]*\s*(?:<[^>]+>)*\s*(https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+)', c)
    if hp:
        out["homepage"] = hp.group(1).rstrip(".,;")
    return out, sections, meta

if __name__ == "__main__":
    man = json.load(open("profile_manifest.json", encoding="utf-8"))
    res = {}
    for rec in man:
        if not rec.get("file"):
            continue
        c = open(os.path.join(PROF, rec["file"]), encoding="utf-8", errors="ignore").read()
        out, sections, meta = parse_common(c)
        out["name"] = rec["name"]
        out["url"] = rec["url"]
        out["site"] = rec["site"]
        out["meta"] = meta
        if "_headings" not in out:
            out["_headings"] = list(sections.keys())
        res[rec["key"]] = out
    json.dump(res, open("profiles_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hr = sum(1 for v in res.values() if v["research"])
    he = sum(1 for v in res.values() if v["email"])
    hp = sum(1 for v in res.values() if v["publications_raw"])
    hh = sum(1 for v in res.values() if v.get("homepage"))
    print("total", len(res), "research", hr, "email", he, "pubs", hp, "homepage", hh)
