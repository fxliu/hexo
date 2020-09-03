---
title: USBHID
tags: 
  - USBHID
categories: 
  - linux
description: USBHID
date: 2020-09-03 10:58:08
updated: 2020-09-03 10:58:08
---

## 工具

+ [hidapi](https://github.com/libusb/hidapi)
+ `es:svn\bar_machine\trunk\C++\EIDSDK\linux\ESCOSSP`

## linux 环境

```sh
# 见README.md
# 失败情况：一般是缺少对应库，yum安装即可
# sudo apt-get install libudev-dev libusb-1.0-0-dev libfox-1.6-dev
# sudo apt-get install autotools-dev autoconf automake libtool
./bootstrap
./configure
make
make install # as root, or using sudo

# libudev-dev
# on ubuntu： apt-get install libudev-dev
# on centos： yum install systemd-devel

make clean
make uninstall

# 只需要编译 linux文件夹 内容即可
`动态库(.so)链接静态库(.a)的情况：.o 生成需要指定 -shared -fPIC`

gcc -o hid.o -I ../hidapi -shared -fPIC -c hid.c
ar -r libhidapi-hidraw.a hid.o
# 编译so时，附加到 -lhidapi-hidraw -ludev 上即可（依赖udev-静态），或者指定 .a 全路径
gcc -o libtest.so test.o -shared -fPIC -Lhidapi -lhidapi-hidraw -ludev
g++ -o libESCOSSP.so ESCOSSP.o ***.o hidapi/libhidapi-hidraw.a -ludev -shared -fPIC
```
