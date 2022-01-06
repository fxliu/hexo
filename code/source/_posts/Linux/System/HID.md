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

```sh
# SV806环境备记 - 基于udev
./bootstrap
./configure --host=arm-himix200-linux --prefix=/opt/hisi-linux/x86-arm/arm-himix200-linux/target/usr CC=/opt/hisi-linux/x86-arm/arm-himix200-linux/bin/arm-himix200-linux-gcc CXX=/opt/hisi-linux/x86-arm/arm-himix200-linux/bin/arm-himix200-linux-g++
# 补充环境 - README.txt
sudo apt-get install libudev-dev libusb-1.0-0-dev libfox-1.6-dev
sudo apt-get install autotools-dev autoconf automake libtool
# 只编译linux版
cd linux
make
make install
```

## udev

```sh
# https://mirrors.edge.kernel.org/pub/linux/utils/kernel/hotplug/
./configure --host=arm-linux-gnueabihf --prefix=./build CC=arm-linux-gnueabihf-gcc AR=arm-linux-gnueabihf-ar
# 依赖 blkid ，编译失败

# https://github.com/gentoo/eudev
# release：http://dev.gentoo.org/~blueness/eudev/
./autogen.sh
./configure --host=arm-linux-gnueabihf --prefix=/home/lfx/eudev-master/build CC=arm-linux-gnueabihf-gcc AR=arm-linux-gnueabihf-ar --disable-blkid --disable-kmod
```

```sh
# SV806环境备记
./configure --host=arm-himix200-linux --prefix=/opt/hisi-linux/x86-arm/arm-himix200-linux/target/usr CC=/opt/hisi-linux/x86-arm/arm-himix200-linux/bin/arm-himix200-linux-gcc CXX=/opt/hisi-linux/x86-arm/arm-himix200-linux/bin/arm-himix200-linux-g++ --disable-manpages 
# 编译整个eudev-3.2.2
make
# 只安装./src/libudev
cd libudev
make install
```
