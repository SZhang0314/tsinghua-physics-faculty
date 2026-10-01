# -*- coding: utf-8 -*-
import re
c = open('data/raw/ias-faculty.html', encoding='utf-8').read()
print('LEN', len(c))
for kw in ['teacher-name', 'teacher', 'info/', '教员', '研究员', '教授', '院士', '姓名', '主任', 'vsb_content']:
    print(kw, c.count(kw))
i = c.find('vsb_content')
seg = c[i:i+6000] if i > 0 else c[:6000]
open('tmp_ias.txt', 'w', encoding='utf-8').write(seg)
