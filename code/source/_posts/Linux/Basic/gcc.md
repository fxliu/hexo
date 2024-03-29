---
title: gcc
tags: 
  - gcc
categories: 
  - linux
description: gcc
date: 2021-09-17 15:09:16
updated: 2021-09-17 15:09:16
---

## 编译

`sudo gcc **.cpp -g0 -fPIC -shared -fvisibility=hidden -fvisibility-inlines-hidden -fno-stack-protector -o lib**.so -Wl,--strip-all -Wl,-z,noexecstack`

## Release

+ 无调试信息
  + `-g0`
+ 忽略所有符号信息
  + `-Wl,--strip-all`
  + 尾缀到-o 后面
+ 不需要可执行堆栈
  + `-Wl,-z,noexecstack`

## 取消 栈溢出保护机制

+ `-fno-stack-protector`

## 依赖库

+ 查看依赖的库
  + `objdump -x xxoo.so | grep NEEDED`
+ 查看缺失的库
  + `ldd xxoo.so`
