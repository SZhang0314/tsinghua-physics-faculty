# -*- coding: utf-8 -*-
import re
for f in ["ep-senior", "ep-assoc", "ep-mid"]:
    c = open("data/raw/%s.html" % f, encoding="utf-8").read()
    # count teacher blocks
    n = c.count('class="teacher-name"')
    # look for pagination
    page_links = re.findall(r'href="([^"]*(?:page|Page|list|index)[^"]*\d+[^"]*)"', c)
    print(f, "teacher-blocks=", n, "len=", len(c))
    # find page numbers
    nums = re.findall(r'共\s*(\d+)\s*[页条人]', c)
    print("  totals:", nums)
    # find all hrefs in a pagination-like div
    pg = re.findall(r'(?:page|next|下一页|尾页)[^>]{0,40}', c)
    print("  pgkeys:", pg[:10])
