(function ($) {
    var index_head_tpl = '<tr class="index-head"><td colspan="2">旧文件:{old_file}</td><td colspan="2">新文件:{new_file}</td></tr>';
    var seg_head_tpl = '<tr class="seg-head"><td colspan="2">>>>行号:{left_start_line}, 行数:{left_count}</td><td colspan="2">>>>行号:{right_start_line}, 行数:{right_count}</td></tr>';
    var row_tpl = '<tr><td class="{left_type} line-td">{left_line}</td><td class="{left_type}">{left_row}</td><td class="{right_type} line-td">{right_line}</td><td class="{right_type}">{right_row}</td></tr>';

    function generate_index_head(index) {
        var tpl = index_head_tpl
        return tpl.replace(/{old_file}/g, index.old_file).replace(/{new_file}/g, index.new_file)
    }

    function generate_seg_head(seg) {
        var tpl = seg_head_tpl
        return tpl.replace(/{left_start_line}/g, seg.left_start_line).replace(/{left_count}/g, seg.left_count).replace(/{right_start_line}/g, seg.right_start_line).replace(/{right_count}/g, seg.right_count)
    }

    function generate_row(row) {
        var tpl = row_tpl;
        return tpl.replace(/{left_line}/g, row.left_line).replace(/{left_row}/g, $('<div>').text(row.left_row).html()).replace(/{left_type}/g, row.left_type).replace(/{right_line}/g, row.right_line).replace(/{right_row}/g, $('<div>').text(row.right_row).html()).replace(/{right_type}/g, row.right_type)
    }

    $.fn.diffview = function(view_data) {
        for (var i = 0; i < view_data.length; ++i) {
            // 每个文件是一个table
            var index = view_data[i]
            var table = $('<table class="side-by-side-table">')

            // 用于控制样式的占位
            table.append($('<colgroup class="line-td">'))
            table.append($('<colgroup>'))
            table.append($('<colgroup class="line-td">'))
            table.append($('<colgroup>'))

            // 表格头
            table.append($(generate_index_head(index)))

            // 文件内每个段落
            var segs = index.segments;
            for (var j = 0; j < segs.length; ++j) {
                var seg = segs[j];
                table.append($(generate_seg_head(seg)))
                for (var k = 0; k < seg.rows.length; ++k) {
                    var row = seg.rows[k];
                    table.append($(generate_row(row)))
                }
            }
            this.append($("<h2>").text(index.index_name)).append(table)
        }
    }
})(jQuery)
