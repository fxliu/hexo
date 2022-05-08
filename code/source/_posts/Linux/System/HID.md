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

## linux HID驱动支持

```sh
# 查看USB设备
lsusb
# 查看支持的所有类型
ls /dev

# 设备类型: hidraw, /dev/hidraw0 | /dev/hidraw1
ls /dev/hidraw*

# 设备类型: hiddev, 非标准的输入设备
ls /dev/usb/hiddev*

# hidraw: 原生人机交互设备, 应用通过原生接口直接与设备通讯
# hiddev: 非标准设备解析器, 应用经过hiddev(解析器)与设备通讯
```

## eudev

```sh
tar -xvf eudev-3.2.2.tar.xz

./configure --host=arm-linux --disable-manpages --prefix=/opt/rk3288/arm-linux-gnueabihf/libc/usr CC=/opt/rk3288/bin/arm-linux-gnueabihf-gcc

# 编译整个eudev-3.2.2
make
# 只安装./src/libudev
cd ./src/libudev
make install
```

## hidapi

```sh
tar -xvf hidapi-b5b2e1779b6cd2edda3066bbbf0921a2d6b1c3c0.tar.xz

# 补充环境 - README.txt
sudo apt-get install autotools-dev autoconf automake libtool
sudo apt-get install libudev-dev libusb-1.0-0-dev libfox-1.6-dev

# 设置参数: 也可以改为命令行赋值参数:make PREFIX=/opt/arm-xmv2-linux/usr
export CROSS=/opt/rk3288/bin/arm-linux-gnueabihf-
export PREFIX=/opt/rk3288/arm-linux-gnueabihf/libc/usr

# 只编译linux版
cd linux
make -f hidapi-Makefile
make -f hidapi-Makefile install
```

```Makefile
# hidapi-Makefile
# -------------------------------------------------------
# CROSS  := 交叉编译环境路径
# PREFIX := 安装路径

CC       := $(CROSS)gcc
INCLUDES := -I$(PREFIX)/include
LIBS_UDEV:= -L$(PREFIX)/lib
# -------------------------------------------------------

all: libs

libs: libhidapi-hidraw.so

CC       ?= gcc
CFLAGS   ?= -Wall -g -fpic

LDFLAGS  ?= -Wall -g

COBJS     = hid.o
OBJS      = $(COBJS)
LIBS_UDEV += -ludev -lrt
LIBS      = $(LIBS_UDEV)
INCLUDES  += -I../hidapi

# Shared Libs
libhidapi-hidraw.so: $(COBJS)
	$(CC) $(LDFLAGS) $(LIBS_UDEV) -shared -fpic -Wl,-soname,$@.0 $^ -o $@

# Objects
$(COBJS): %.o: %.c
	$(CC) $(CFLAGS) -c $(INCLUDES) $< -o $@

install:
	mv -f ./libhidapi-hidraw.so $(PREFIX)/lib
	cp -rf ../hidapi $(PREFIX)/include

clean:
	rm -f $(OBJS) libhidapi-hidraw.so

.PHONY: clean libs
```
