---
title: 工具集
tags: 
  - tools
categories: 
  - Python
description: tools, pyinstaller
date: 2019‎-10-31 ‏‎‏‎‏‎09:07:37
updated: 2019‎-10-31 ‏‎‏‎‏‎09:07:37
---

## 工具集

+ 脚本编译成可执行文件
  + pyinstaller: `pip install pyinstaller`
    + 编译成单个文件
      + `pyinstaller -F t.py`
    + 编译到目录，公共模块会提取成dll
      + `pyinstaller t.py`
      + `pyinstaller -D t.py`
    + 其他参数
      + -p：指定python安装包路径
      + -i：指定图标
      + –noconsole，就是无窗口运行
