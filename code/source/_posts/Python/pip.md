---
title: pip
tags: 
  - pip
categories: 
  - Python
description: pip
date: 2019-10-31 09:07:37
updated: 2019-10-31 09:07:37
---

## 虚拟环境

```sh
# venv
apt -y install python3-venv

# 创建虚拟环境
python3 -m venv ./my_venv
# 激活
source ./my_venv/bin/activate
# 退出
deactivate
```

## 国内镜像

+ 清华镜像: https://pypi.tuna.tsinghua.edu.cn/simple
+ 中科大镜像: https://pypi.mirrors.ustc.edu.cn/simple
+ 阿里镜像: https://mirrors.aliyun.com/pypi/simple/
+ 百度镜像: https://mirror.baidu.com/pypi/simple

```sh
# 命令行配置
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set install.trusted-host mirrors.aliyun.com
# 直接操作文件
pip config edit --editor gedit
pip config edit --editor notepad
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
# 查看配置
pip config list
```

