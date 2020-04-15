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
// json对象 -> js字符串
json_str = JSON. stringify(js_obj);

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

tools.dateFormat = function (date, fmt = 'YYYY-MM-DD HH:mm:ss') {
    if (!date) {
        return '';
    }
    if (typeof date === 'string') {
        date = new Date(date.replace(/-/g, '/'));
    }
    if (typeof date === 'number') {
        date = new Date(date);
    }
    let o = {
        'M+': date.getMonth() + 1,
        'D+': date.getDate(),
        'h+': date.getHours() % 12 === 0 ? 12 : date.getHours() % 12,
        'H+': date.getHours(),
        'm+': date.getMinutes(),
        's+': date.getSeconds(),
        'q+': Math.floor((date.getMonth() + 3) / 3),
        'S': date.getMilliseconds()
    };
    let week = {
        '0': '\u65e5',
        '1': '\u4e00',
        '2': '\u4e8c',
        '3': '\u4e09',
        '4': '\u56db',
        '5': '\u4e94',
        '6': '\u516d'
    };
    if (/(Y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    if (/(E+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? '\u661f\u671f' : '\u5468') : '') + week[date.getDay() + '']);
    }
    for (let k in o) {
        if (new RegExp('(' + k + ')').test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)));
        }
    }
    return fmt;
};
```

## 对象

```js
var obj = {'0':'a','1':'b','2':'c'};
for(var i in obj) {
     console.log(i,":",obj[i]);
}
```
