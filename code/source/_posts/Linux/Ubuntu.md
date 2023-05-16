---
title: Ubuntu
tags: 
  - Ubuntu
categories: 
  - linux
description: Ubuntu
date: 2022-06-22 16:45:50
updated: 2022-06-22 16:45:50
---

## 虚拟机工具

```bash
# Ubuntu 20 以上已经支持命令行安装了
sudo apt-get autoremove open-vm-tools
sudo apt-get install open-vm-tools
sudo apt-get install open-vm-tools-desktop
sudo reboot
```

### 阿里源

+ 可能导致包依赖环境异常，尽量不使用

```sh
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo gedit /etc/apt/sources.list
sudo apt-get update
sudo apt-get upgrade
# 20.04 - focal
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
# 22.04 - jammy
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
```

## ssh

```sh
sudo apt-get install openssh-server
sudo systemctl status ssh   # q退出

sudo systemctl enable ssh
sudo systemctl disable ssh
```

## Android-NDK

```sh
# 旧版本NDK下载地址: https://developer.android.google.cn/ndk/downloads/older_releases?hl=zh-cn

# NDK下载安装
wget -c http://dl.google.com/android/ndk/android-ndk-r10e-linux-x86_64.bin
chmod 777 android-ndk-r10c-linux-x86_64.bin
# bin文件直接执行就是解压缩, 如果是zip包直接解压即可
./android-ndk-r10c-linux-x86_64.bin

# 当前用户环境变量
sudo gedit ~/.bashrc
export NDK=/home/sun/ijkPlayer/android-ndk-r10e
export PATH=${PATH}:$NDK
# 保存并使之生效
source  ~/.bashrc
# 验证 - 指令存在即认为好使
ndk-build
```

```sh
# SDK下载安装
sudo apt install android-sdk
sudo apt install android-tools-adb
sudo apt install android-tools-fastboot
```
