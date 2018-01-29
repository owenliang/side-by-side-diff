# -*- coding: utf-8 -*-

import difflib

# 1, 从stdin读svn diff内容
# 2, 解析diff为若干index, 每个index内为多个diff_segment, 每个diff_segment复原出left segment与right_segment
# 3, 将left_segment与right_segment传给difflib._mdiff, 得到side-by-side列表
# 4, 根据side-by-side列表, 生成html视图

