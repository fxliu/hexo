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

+ Assert        FF6B68
+ Debug         3AB3FB
+ Error         FC3630
+ Info          30b051
+ Verbose       BBBBBB
+ Warning       FDBA2C

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

## 日志过滤

+ 过滤特定内容的日志: `^(.*(XXX|YYY)).*$`
    + ^ 匹配字符串开始位置
    + . 匹配除换行符 \n 之外的任何单字符
    + * 匹配前面的子表达式零次或多次
    + () 表示一个字表达式的开始与结束
    + | 指明两项之间的一个选择，可以理解为或，多个内容可依次添加
    + $ 匹配字符串结束位置

+ 屏蔽特定内容的日志: `^(?!.*(AAA|BBB)).*$`
    + ?! 表示非捕获元，匹配后面不是我们指定的内容的字符