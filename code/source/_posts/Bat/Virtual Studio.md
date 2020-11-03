---
title: VS
tags:
  - VS
categories:
  - BAT
description: VS
date: 2020-10-25 10:02:30
updated: 2020-10-25 10:02:30
---

## 编译

```bat
@echo off
cd /d "D:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\Common7\IDE"
:: 指定项目
devenv.com esaio.sln /Build "Debug|x64" /project esaio
:: 所有项目
devenv.com esaio.sln /Build "Debug|x64"
:: 清理
devenv.com esaio.sln /Clean "Debug|x64"
```

```bat

```
