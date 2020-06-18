---
title: CSS基础
tags: 
  - 基础
categories: 
  - CSS
description: 基础
date: 2019-11-14 19:04:37
updated: 2019-11-14 19:04:37
---

## 背景图

```css
div {
    width: 160px;
    height: 160px;
    background-size: cover;
    background-image: 'url(' + url/base64 + ')';
    background-repeat: no-repeat;   /* 不重复 */
    background-position: center;    /* 居中显示 */
    filter: opacity(0.95);          /* 透明度 */
}
background-size: 63px;  /* 指定大小：第二个参数默认auto */
background-size: %50;   /* 指定大小：第二个参数默认auto */
background-size: cover;     /* 等比拉伸 */
background-size: contain;   /* 拉伸 */
background-position
```

## 动态效果

```less
.btn {
    color: #10aeff;
    &:active {
        color: #181741;
    }
    &:visited {
        color: #181741;
    }
}
```
