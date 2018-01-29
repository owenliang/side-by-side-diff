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
        diff_seg = {'left_segment': [], 'right_segment': [], 'left_start_line': match_result.group(1), 'right_start_line': match_result.group(4)}
        indexes[-1]['diff_segment'].append(diff_seg)
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

# 4, 生成用于渲染的side-by-side列表(TODO: 处理多个index文件)
view_data = []
for index in indexes:
    for diff_segment in index['diff_segment']:
        for side_by_side_segment in diff_segment['side_by_side_segment']:
            row_data = {
                'left_line': side_by_side_segment[0][0],
                'left_row': side_by_side_segment[0][1],
                'right_line': side_by_side_segment[1][0],
                'right_row': side_by_side_segment[1][1],
            }
            # TODO: 需要判断row.startswith(), 进行染色与截断
            if row_data['left_line']: # 非空白行
                row_data['left_row'] = row_data['left_row'][2:-1].rstrip("\n")
                row_data['left_line'] = int(diff_segment['left_start_line']) + row_data['left_line'] - 1
            if row_data['right_line']: # 非空白行
                row_data['right_row'] = row_data['right_row'][2:-1].rstrip("\n")
                row_data['right_line'] = int(diff_segment['right_start_line']) + row_data['right_line'] - 1
            view_data.append(row_data)

# 5, 生成table布局
html_dom = ["<head><meta charset='utf-8'></head><body><table>"]
row_template = '<tr><td>{left_line}</td><td>{left_row}</td><td>{right_line}</td><td>{right_row}</td></tr>'
for row_data in view_data:
    row = row_template[:].replace('{left_line}', str(row_data['left_line'])).replace('{left_row}', row_data['left_row']).replace('{right_line}', str(row_data['right_line'])).replace('{right_row}', row_data['right_row'])
    html_dom.append(row)
html_dom.append("</table></body>")

# 6, 写到html文件在中
with open('diff.html', 'w') as fd:
    html = ''.join(html_dom)
    fd.write(html)


