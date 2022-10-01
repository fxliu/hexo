---
title: gcc
tags: 
  - gcc
categories: 
  - linux
description: gcc
date: 2022-06-06 19:12:20
updated: 2022-06-06 19:12:20
---

## 基础规则

+ 无调试信息
  + `-g0`
+ 忽略所有符号信息
  + `-Wl,--strip-all`
  + 尾缀到-o 后面
+ 不需要可执行堆栈
  + `-Wl,-z,noexecstack`
+ 取消 栈溢出保护机制
  + `-fno-stack-protector`

```sh
gcc EsWlt.cpp -g0 -fPIC -shared -fvisibility=hidden -fvisibility-inlines-hidden -fno-stack-protector -o libwlt.so -Wl,--strip-all
```

## 依赖库

+ 查看依赖的库
  + `objdump -x xxoo.so | grep NEEDED`
  + `readelf -d es_idcard_demo`
+ 查看缺失的库
  + `ldd xxoo.so`
+ 查看导出
  + `nm -D xxxoo.so`
