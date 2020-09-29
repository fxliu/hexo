---
title: adb
tags: 
    - adb
categories: 
    - Android
description: adb
date: 2020-09-25 15:53:56
updated: 2020-09-25 15:53:56
---

## 基本使用

```bat
:: https://developer.android.google.cn/studio/command-line/adb

:: 查看设备
adb devices
adb devices -l

List of devices attached
emulator-5554 device
emulator-5555 device

:: shell指令
adb -s emulator-5555 shell ls
:: 单个设备时，可以不指定-s
adb shell ls
adb shell lsusb

:: 保留在shell中
adb shell
```
