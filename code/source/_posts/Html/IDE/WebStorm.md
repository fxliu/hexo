---
title: WebStorm
tags: 
  - WebStorm
categories: 
  - IDE
description: WebStorm
date: 2020-05-29 09:52:05
updated: 2020-05-29 09:52:05
---

## 基础

```js
// 识别 @，创建 webpack.conf.js
'use strict';
const path = require('path');

function resolve(dir) {
  return path.join(__dirname, '.', dir)
}

module.exports = {
  context: path.resolve(__dirname, './'),
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      '@': resolve('src'),
      // '@assets': resolve('src/assets'),
      // '@layouts': resolve('src/layouts'),
      // '@pages': resolve('src/pages'),
      // '@comp': resolve('src/components'),
      // '@api': resolve('src/api'),
      // '@plug': resolve('src/plugins'),
      // '@utils': resolve('src/utils')
    }
  }
};
```

## .EditorConfig

```ini
# 表明是最顶层的配置文件
root = true

# 文件类型，可以是 *.js *.html
[*]
# 编码
charset = utf-8
# 缩进 tab | space
indent_style = tab
# 缩进占位
indent_size = 4
# 行尾回车符统一 lf | cr | crlf
end_of_line = lf
# 使文件以一个空白行结尾
insert_final_newline = true
# 除去换行行首的任意空白字符
trim_trailing_whitespace = true

```
