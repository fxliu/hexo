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
```

```js
// 日期
let d1 = new Date('2010-02-12');
d1.setFullYear(d.getFullYear()+10);
// 毫秒
let date = new Date();
console.log(date, date.getMilliseconds());
// 时间戳
Math.floor(new Date() / 1000);
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
export function parseTime(time, cFormat = '{y}-{m}-{d} {h}:{i}:{s}') {
  if (arguments.length === 0) {
    return null
  }
  const format = cFormat || '{y}-{m}-{d} {h}:{i}:{s}'
  let date
  if (typeof time === 'object') {
    date = time
  } else {
    if ((typeof time === 'string') && (/^[0-9]+$/.test(time))) {
      time = parseInt(time)
    }
    if ((typeof time === 'number') && (time.toString().length === 10)) {
      time = time * 1000
    }
    date = new Date(time)
  }
  const formatObj = {
    y: date.getFullYear(),
    m: date.getMonth() + 1,
    d: date.getDate(),
    h: date.getHours(),
    i: date.getMinutes(),
    s: date.getSeconds(),
    a: date.getDay()
  }
  const time_str = format.replace(/{([ymdhisa])+}/g, (result, key) => {
    const value = formatObj[key]
    // Note: getDay() returns 0 on Sunday
    if (key === 'a') { return ['日', '一', '二', '三', '四', '五', '六'][value ] }
    return value.toString().padStart(2, '0')
  })
  return time_str
}


var sdtime1 = new Date('2018-03-22 16:14:55')

var sdtime2 = sdtime1.setHours(sdtime1.getHours() -1)//小时
var sdtime3=new Date().setDate((new Date().getDate()-7))//7天
var sdtime4=new Date().setMonth((new Date().getMonth()-1))//一个月
var sdtime5=new Date().setFullYear((new Date().getFullYear()-1))//一年

```

## 对象

```js
var obj = {'0':'a','1':'b','2':'c'};
for(var i in obj) {
     console.log(i,":",obj[i]);
}
```
