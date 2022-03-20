---
title: Application
tags: 
    - Application
categories: 
    - Android
description: Application
date: 2022-03-20 16:23:01
updated: 2022-03-20 16:23:01
---

## 基础应用

```makefile
# 指定ABI
APP_ABI := armeabi-v7a, arm64-v8a
# APP_ABI := all
# APP_ABI := armeabi, armeabi-v7a, x86, mips, arm64-v8a, mips64, x86_64

# 编译参数
APP_LDFLAGS := -llog
APP_CPPFLAGS += -fexceptions -frtti

# 依赖环境
APP_STL := c++_shared

```
