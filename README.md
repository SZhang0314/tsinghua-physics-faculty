# 清华大学物理方向教师目录 · Tsinghua Physics Faculty Directory

A browsable, searchable directory of physics-related faculty at **Tsinghua University (清华大学)**, covering three departments:

- **物理系 (Department of Physics)** — 84 faculty, across 凝聚态物理 / 原子分子与光物理 / 粒子核天体物理 / 量子信息
- **工程物理系 (Department of Engineering Physics)** — 78 faculty, 核科学与技术 / 粒子物理与核物理 / 医学物理等
- **高等研究院 (Institute for Advanced Study, IASTU)** — 27 faculty, 凝聚态理论 / 冷原子 / 天体物理 / 数学等

## Live page

Open `index.html` directly, or visit the GitHub Pages URL:

> https://szhang0314.github.io/tsinghua-physics-faculty/

Features: full-text search, filter by department / research direction, sort by name / department / title. Each card shows title, research directions, a short research summary, selected publications, and links to the official profile and email.

## Data

- `data/faculty.json` — source of truth, one record per researcher (schema per the `search_prof` skill).
- `data/raw/` — saved HTML snapshots of the official pages used (audit trail).

### Fields

| field | meaning |
|---|---|
| `name` / `name_local` | researcher name (Chinese) |
| `department` | 物理系 / 工程物理系 / 高等研究院 |
| `title` | 教授 / 研究员 / 副教授 … |
| `subject` | broad subject |
| `research_directions` | research-direction chips |
| `focus_areas` | finer sub-directions (physics dept) |
| `summary` | 1–2 sentence research summary (from the official profile) |
| `publications` | up to 5 selected publications parsed from the official profile |
| `homepage` | personal homepage, when listed |
| `profile_url` | official university profile page |
| `email` | listed institutional email |
| `sources` | URLs actually used |
| `confidence` | `fine` (enriched) or `coarse` (roster only) |

## Sources

All data is public and first-party:

- 物理系: https://www.phys.tsinghua.edu.cn/ (教师名录 · 按专业分类 / 导师及研究方向)
- 工程物理系: https://www.ep.tsinghua.edu.cn/szdw/jsdw.htm
- 高等研究院: https://www.ias.tsinghua.edu.cn/yjry/jy.htm

## How to regenerate

```bash
python scrape.py            # fetch directory pages
python scrape_profiles.py   # fetch individual profile pages
python parse_final.py       # extract research / publications / email
python consolidate.py       # build data/faculty.json
python "…/scripts/build_site.py" --data data/faculty.json --out . \
       --title "清华大学物理方向教师目录 · Tsinghua Physics Faculty"
```

## Accuracy notes

- Identity is taken from official department rosters; emails, titles and research text come from the official profile pages.
- `publications` are parsed from the profile's own 主要论著 / 学术成果 section (best-effort); titles may include author lists. No publication is invented.
- Some profiles do not list a personal homepage — `homepage` is omitted rather than guessed.
- Generated: see `generated_at` in `data/faculty.json`.
