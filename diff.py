# -*- coding: utf-8 -*-

import difflib
import sys
import re
from pprint import pprint

# 1, 从stdin读svn diff内容
lines = sys.stdin.readlines()
#for line in lines:
#    print(line, )

# 2, 解析diff为若干index, 每个index内为多个diff_segment, 每个diff_segment复原出left segment与right_segment
indexes = []
for line in lines:
    # 删除\r
    line = line.replace('\r', '')

    # --- yaf/readme.txt	(revision 171415)
    match_result = re.match(r'^---\s*(\S+)', line)
    if match_result:
        indexes.append({
            'old_file': match_result.group(1),
            'diff_segment': []
        })
        continue

    # +++ yaf/readme.txt	(working copy)
    match_result = re.match(r'^\+\+\+\s*(\S+)', line)
    if match_result:
        indexes[-1]['new_file'] = match_result.group(1)
        continue

    # @@ -1,16 +1,18 @@
    match_result = re.match(r'^@@\s*-(\d+)(,(\d+))?\s*\+(\d+)(,(\d+))?\s*@@$', line)
    if match_result:
        indexes[-1]['diff_segment'].append({'left_segment': [], 'right_segment': []})
        continue

    #  -[项目地址]
    match_result = re.match(r'^-', line)
    if match_result:
        indexes[-1]['diff_segment'][-1]['left_segment'].append(line[1:])
        continue

    # +[项目地址,haole]
    match_result = re.match(r'^\+', line)
    if match_result:
        indexes[-1]['diff_segment'][-1]['right_segment'].append(line[1:])
        continue

    # \ No newline at end of file
    match_result = re.match(r'^\\', line)
    if match_result:
        continue;

    #  [框架目标]
    if indexes:
        indexes[-1]['diff_segment'][-1]['left_segment'].append(line[1:])
        indexes[-1]['diff_segment'][-1]['right_segment'].append(line[1:])

# 3, 将left_segment与right_segment传给difflib._mdiff, 得到side-by-side列表
for index in indexes:
    for diff_segment in index['diff_segment']:
        diff_segment['side_by_side_segment'] = list(difflib._mdiff(diff_segment['left_segment'], diff_segment['right_segment']))

# pprint(indexes)

# 4, 根据side-by-side列表, 生成html视图


