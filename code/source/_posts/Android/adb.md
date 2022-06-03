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

:: 网络连接
adb connect 192.168.200.60:5555
```

```bat
:: 安装APK
adb install xx.apk
:: -r 覆盖安装
adb install -r xx.apk
:: 启动
adb shell am start  包名/MainActivity
:: 强制终止
adb shell am force-stop 包名
:: 强制终止 并清理运行产生的数据
adb shell pm clear 包名
```

```bat
:: 文件传输: PC -> Android
adb push <local> <remote>
adb push D:\test.log /data/
:: 文件传输: Android -> PC
adb pull <remote> <local>
```
