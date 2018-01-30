(function ($) {
    var index_head_tpl = '<tr class="index-head"><td colspan="2">{old_file}</td><td colspan="2">{new_file}</td></tr>';
    var seg_head_tpl = '<tr class="seg-head"><td colspan="2">>>>起始行号:{left_start_line}</td><td colspan="2">>>>起始行号:{right_start_line}</td></tr>';
    var row_tpl = '<tr><td>{left_line}</td><td class="{left_type}">{left_row}</td><td class="{right_type}">{right_line}</td><td>{right_row}</td></tr>';

    function generate_index_head(index) {
        var tpl = index_head_tpl
        return tpl.replace('{old_file}', index.old_file).replace('{new_file}', index.new_file)
    }

    function generate_seg_head(seg) {
        var tpl = seg_head_tpl
        return tpl.replace('{left_start_line}', seg.left_start_line).replace('{right_start_line}', seg.right_start_line)
    }

    function generate_row(row) {
        var tpl = row_tpl;
        return tpl.replace('{left_line}', row.left_line).replace('{left_row}', row.left_row).replace('{left_type}', row.left_type).replace('{right_line}', row.right_line).replace('{right_row}', row.right_row).replace('{right_type}', row.right_type)
    }

    $.fn.diffview = function(view_data) {
        for (var i = 0; i < view_data.length; ++i) {
            // 每个文件是一个table
            var index = view_data[i]
            var table = $('<table class="side-by-side-table">')
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
        }
        this.append(table)
    }
})(jQuery)
