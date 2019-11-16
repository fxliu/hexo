---
title: JS基础
tags: 
  - 基础
categories: 
  - JS
description: 基础
date: 2019-11-14 19:04:37
updated: 2019-11-14 19:04:37
---

## 基础

```js
// 模板字符串
let a = 'hello';
let b = `${a} world`;

// json字符串 -> js对象
js_obj = JSON.parse(json_str);

// encodeUrl
function urlEncode(param) {
    var paramStr = '';
    for (let k in param) {
        paramStr += paramStr ? '&':'';
        paramStr += encodeURIComponent(k) + '=' + encodeURIComponent(param[k]);
    }
    return paramStr;
};
```

```js
// 日期
let d1 = new Date('2010-02-12');
d1.setFullYear(d.getFullYear()+10);
// 毫秒
let date = new Date();
console.log(date, date.getMilliseconds());
// vux的日期格式化
import {dateFormat} from 'vux';
let d2 = dateFormat(d, 'YYYY-MM-DD');
```

## 数组

```js
// 遍历
for(let j = 0,len=arr.length; j < len; j++) {
}
// 清空
arr.splice(0,arr.length);
```

## 对象

```js
var obj = {'0':'a','1':'b','2':'c'};
for(var i in obj) {
     console.log(i,":",obj[i]);
}
```
