---
title: JQuery
tags: 
  - JQuery
categories: 
  - JS
description: JQuery
date: 2019-11-14 19:04:37
updated: 2019-11-14 19:04:37
---

## 基础

```js
function ajaxGet(url, data) {
    const _this = this;
    $.get(url, data, function (data, status) {
        myPrint("状态：" + status);
        myPrint("数据：" + data);
        // 这里的this是ajax的this, 要使用外层this需要自己定义变量保存
        _this.content = data;
    })
}

function ajaxPost(url, data, param={}) {
    if(param)
        url += "?" + $.param(param);
    $.post(url, data, function (data, status) {
        myPrint("状态：" + status);
        myPrint("数据：" + data);
    })
}
let d = {
    a: "1",
    b: "2",
};
ajaxGet('/uri', d);
```
