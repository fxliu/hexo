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
:: apk安装包 -> 查看包名
aapt dump badging D:\test\xxx.apk
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
adb push D:\test.log /storage/emulated/0/
:: 文件传输: Android -> PC
adb pull <remote> <local>
```

## 内存溢出

```sh
# 查看所有支持项
dumpsys –l

# meminfo
# https://www.proyy.com/7006950034935660574.html
dumpsys meminfo com.eseid.eid_idcard_svr.watch
dumpsys meminfo com.eseid.eid_idcard_svr.eid

# 查看到系统所有的注册信息
dumpsys content

# 获取所有进程的内存使用的排行榜
procrank

# 查看更加详细的内存信息
cat /proc/meminfo

# 查看可用内存，缺省单位KB。该命令比较简单、轻量，专注于查看剩余内存情况。
free

showmap
```
