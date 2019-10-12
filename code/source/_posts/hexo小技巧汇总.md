---
title: hexo小技巧汇总
date: 2019-09-01 17:14:57
tags: 
  - hexo
categories: 
  - 博客
---

## hexo

### 常用命令

+ 新文章
  + `hexo new [layout] <title>`：`layout`默认`post`

### 代码块不显示行号

+ 调整根目录`_config.yml`配置文件
+ `line_number`默认`true`显示行号，影响代码复制

```yml
highlight:
  line_number: false
```

## fexo

+ 调整根目录`_config.yml`配置文件
+ `busuanzi: true`开启网站统计
  + js代码：`fexo\layout\_partial\head.ejs`
+ `baidu_analytics: ****`百度网站统计
  + js代码：`fexo\layout\_partial\baidu-analytics.ejs`
    + 补充类型字段`hm.type = "*.*";`，避免部分浏览器加载失败
  + 百度推送：`fexo\layout\_partial\baidu-analytics.ejs`
