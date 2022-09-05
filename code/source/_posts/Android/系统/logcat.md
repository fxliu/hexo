---
title: logcat
tags: 
    - logcat
categories: 
    - Android
description: logcat
date: 2022-09-01 15:45:17
updated: 2022-09-01 15:45:17
---

## base

```sh
# 系统环境参数 - 查看
adb shell getprop > 1.log
# 系统环境参数 - 设置
adb shell setprop debug.facepass.log.level 2

# 提取日志
adb shell logcat
```

## logcat

```sh
# 获取所有日志, 并阻塞持续新日志
logcat
# 获取所有日志并推出, 非阻塞
logcat -d

# 环形缓冲区的大小并退出
logcat -g
# 请求不同的环形缓冲区 ('main', 'system', 'radio', 'events',默认为"-b main -b system")
logcat -b <buffer> 

# 输出到文件
logcat -f <filename>
# 指定日志缓冲大小, 配合-f使用, 默认16k
logcat -f <filename> -r [<kbytes>]
# 指定日志文件个数, 配合-f使用, 默认4
logcat -f <filename> -r [<kbytes>] -n <count>

# 清理所有日志
logcat -c
```

### logcat -s 过滤器

```sh
logcat -s <tag>[:priority]
logcat -s *:D       # 所有>=Debug日志
logcat -s healthd:D # 指定tag

# priority
V Verbose
D Debug
I Info
W Warn
E Error
F Fatal
S Silent
```
