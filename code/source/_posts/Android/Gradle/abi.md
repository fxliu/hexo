---
title: abi
tags: 
    - abi
categories: 
    - Android
description: abi
date: 2022-07-09 23:12:03
updated: 2022-07-09 23:12:03
---

## build.gradle(:app)

```gradle
android {
    defaultConfig {
        ndk {
            // speed up build: compile only arm versions
            // armeabi, armeabi-v7a, x86, mips, arm64-v8a, mips64, x86_64
            abiFilters 'armeabi-v7a', 'arm64-v8a'
        }
    }
}
```

## Application.mk

```mk
# ndk.abiFilters 描述打包支持abi
# Application.mk 描述so支持abi，理论上需要保持一致
APP_ABI := armeabi-v7a arm64-v8a
```
