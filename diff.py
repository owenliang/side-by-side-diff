# -*- coding: utf-8 -*-

import difflib
import sys
import re
from pprint import pprint
import json

# 1, 从stdin读svn diff内容
lines = sys.stdin.readlines()

# 2, 解析diff为若干index, 每个index内为多个diff_segment, 每个diff_segment复原出left segment与right_segment
indexes = []
for line in lines:
    # 删除\r
    line = line.replace('\r', '')

    # Index: favicon.ico
    match_result = re.match(r'^Index:\s*', line)
    if match_result:
        indexes.append({'diff_segment': []})
        continue

    # --- yaf/readme.txt	(revision 171415)
    match_result = re.match(r'^---\s*(\S+)', line)
    if match_result:
        indexes[-1]['old_file'] = match_result.group(1)
        continue

    # +++ yaf/readme.txt	(working copy)
    match_result = re.match(r'^\+\+\+\s*(\S+)', line)
    if match_result:
        indexes[-1]['new_file'] = match_result.group(1)
        continue

    # @@ -1,16 +1,18 @@
    match_result = re.match(r'^@@\s*-(\d+)(,(\d+))?\s*\+(\d+)(,(\d+))?\s*@@$', line)
    if match_result:
        diff_seg = {'left_segment': [], 'right_segment': [], 'left_start_line': match_result.group(1), 'right_start_line': match_result.group(4)}
        indexes[-1]['diff_segment'].append(diff_seg)
        continue

    # 没有segment上下文
    if not indexes[-1]['diff_segment']:
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
    if indexes and indexes[-1]['diff_segment']: # 跳过一些二进制文件操作, 它们没有segment上下文
        indexes[-1]['diff_segment'][-1]['left_segment'].append(line[1:])
        indexes[-1]['diff_segment'][-1]['right_segment'].append(line[1:])

#pprint(indexes)

# 3, 将left_segment与right_segment传给difflib._mdiff, 得到side-by-side列表
for index in indexes[:]:
    # 删除没有segment的index
    if not index['diff_segment']:
        indexes.remove(index)
        continue
    for diff_segment in index['diff_segment']:
        diff_segment['side_by_side_segment'] = list(difflib._mdiff(diff_segment['left_segment'], diff_segment['right_segment']))

# 4, 生成用于渲染的side-by-side列表
def decorate_row(row, is_deleted):
    out = ''
    while row:
        #  '\0+' -- marks start of added text
        #  '\0-' -- marks start of deleted text
        # '\0^' -- marks start of changed text
        if row.startswith('\0+') or row.startswith('\0-' ) or row.startswith('\0^'):
            row = row[2:]
        elif row.startswith('\1'):  # '\1' -- marks end of added/deleted/changed text
            row = row[1:]
        else: # 未变化的内容
            out += row[0]
            row = row[1:]
    return out, 'deleted' if is_deleted else 'added'

view_data = []
for index in indexes:
    view_data.append({'old_file': index['old_file'], 'new_file': index['new_file'], 'segments': []})
    for diff_segment in index['diff_segment']:
        view_data[-1]['segments'].append({'left_start_line': diff_segment['left_start_line'], 'right_start_line': diff_segment['right_start_line'], 'rows': []})
        for side_by_side_segment in diff_segment['side_by_side_segment']:
            row_data = {
                'left_line': side_by_side_segment[0][0],
                'left_row': side_by_side_segment[0][1],
                'left_type': 'blank' if side_by_side_segment[2] else 'context',
                'right_line': side_by_side_segment[1][0],
                'right_row': side_by_side_segment[1][1],
                'right_type': 'blank' if side_by_side_segment[2] else 'context',
            }

            # 非留白的左侧行
            if row_data['left_line']:
                if row_data['left_type'] == 'blank':
                    row_data['left_row'], row_data['left_type'] = decorate_row(row_data['left_row'], True)
                row_data['left_line'] = int(diff_segment['left_start_line']) + row_data['left_line'] - 1
            # 非留白的右侧行
            if row_data['right_line']:
                if row_data['right_type'] == 'blank':
                    row_data['right_row'], row_data['right_type'] = decorate_row(row_data['right_row'], False)
                row_data['right_line'] = int(diff_segment['right_start_line']) + row_data['right_line'] - 1
            view_data[-1]['segments'][-1]['rows'].append(row_data)

# 5, json序列化到文件
with open('diff.json', 'w') as fp:
    json_str = json.dump(view_data, fp)


