# side-by-side-diff

[什么是side-by-side-diff?](https://owenliang.github.io/side-by-side-diff/sample/side-by-side-view.html)

# how to use ?

执行如下命令，将生成diff.json，可以直接拿来做HTML页面渲染:

```
svn diff | python diff.py
```

# sample 

* diff.json: 用于渲染HTML的数据, 可以直接使用
* diff.patch: svn diff的输出示例
* diffview.js: 前端jquery封装, 可以画出一个默认的table布局
* diffview.css: 前端css封装, 美化diffview.js产生的table布局
* side-by-side-view.html: 容器页面, 容纳diffview.js输出的table布局