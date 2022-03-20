---
title: Android
tags: 
    - Android
categories: 
    - Android
description: Android
date: 2022-03-20 16:23:01
updated: 2022-03-20 16:23:01
---

## 基础应用

```makefile
# 定义变量: 文件当前路径
LOCAL_PATH:= $(call my-dir)
# 编译参数指定: 隐藏符号
LOCAL_CFLAGS += -fvisibility-inlines-hidden -fvisibility=hidden -fno-common
LOCAL_CPPFLAGS += -std=c++11 -fvisibility-inlines-hidden -fvisibility=hidden -fno-common
# 引入其他mk
include $(LOCAL_PATH)/lib_**_sdk.mk
```

```makefile
# APP_ABI: armeabi, armeabi-v7a, x86, mips, arm64-v8a, mips64, x86_64
# APP_ABI: 在Application中指定

# 引入第三方库 - 前置
# -----------------------------------------------------------------------------
# libcrypto
include $(CLEAR_VARS)
LOCAL_SRC_FILES := ./libs/$(APP_ABI)/libcrypto.a
LOCAL_MODULE := crypto
include $(PREBUILT_STATIC_LIBRARY)
# -----------------------------------------------------------------------------
# libssl
include $(CLEAR_VARS)
LOCAL_SRC_FILES := ./libs/$(APP_ABI)/libssl.a
LOCAL_MODULE := ssl
include $(PREBUILT_STATIC_LIBRARY)
# -----------------------------------------------------------------------------
# 重置参数
include $(CLEAR_VARS)

LOCAL_SRC_FILES := \
  $(LIBUSB_ROOT_REL)/native.cpp

# libusb
LOCAL_SRC_FILES += \
  $(LIBUSB_ROOT_REL)/libusb/core.c \
  $(LIBUSB_ROOT_REL)/libusb/descriptor.c \
  $(LIBUSB_ROOT_REL)/libusb/hotplug.c \
  $(LIBUSB_ROOT_REL)/libusb/io.c \
  $(LIBUSB_ROOT_REL)/libusb/sync.c \
  $(LIBUSB_ROOT_REL)/libusb/strerror.c \
  $(LIBUSB_ROOT_REL)/libusb/os/linux_usbfs.c \
  $(LIBUSB_ROOT_REL)/libusb/os/events_posix.c \
  $(LIBUSB_ROOT_REL)/libusb/os/threads_posix.c \
  $(LIBUSB_ROOT_REL)/libusb/os/linux_netlink.c

# hidapi
LOCAL_SRC_FILES += \
  $(LIBUSB_ROOT_REL)/hidapi/hidapi.c \
  $(LIBUSB_ROOT_REL)/hidapi/es_hidapi.cpp

# jsoncpp
LOCAL_SRC_FILES += \
  $(LIBUSB_ROOT_REL)/json/json_reader.cpp \
  $(LIBUSB_ROOT_REL)/json/json_value.cpp \
  $(LIBUSB_ROOT_REL)/json/json_writer.cpp

# mongoose
LOCAL_SRC_FILES += \
  $(LIBUSB_ROOT_REL)/mongoose/mongoose.c

# include
LOCAL_C_INCLUDES += \
  $(LOCAL_PATH) \
  $(LIBUSB_ROOT_ABS)/libusb \
  $(LIBUSB_ROOT_ABS)/libusb/os \
  $(LIBUSB_ROOT_ABS)/hidapi \
  $(LIBUSB_ROOT_ABS)/mongoose \
  $(LIBUSB_ROOT_ABS)/Platform \
  $(LIBUSB_ROOT_ABS)/Public \
  $(LIBUSB_ROOT_ABS)/SdkPublic \
  $(LIBUSB_ROOT_ABS)/EsUsbHid \
  $(LIBUSB_ROOT_ABS)/EsUsbJava \
  $(LIBUSB_ROOT_ABS)/EsUsbUart \
  $(LIBUSB_ROOT_ABS)/EsEidSdk

LOCAL_EXPORT_C_INCLUDES := \
  $(LIBUSB_ROOT_ABS)/libusb \
  $(LIBUSB_ROOT_ABS)/openssl
# 编译参数
LOCAL_CFLAGS := -pthread
LOCAL_CFLAGS += -fvisibility-inlines-hidden -fvisibility=hidden -fno-common
LOCAL_CPPFLAGS := -std=c++11 -fvisibility-inlines-hidden -fvisibility=hidden -fno-common
# 系统库
LOCAL_LDLIBS := -llog
# 第三方库
LOCAL_STATIC_LIBRARIES := ssl crypto
# 目标名称
LOCAL_MODULE := lib_eididcard_sdk
include $(BUILD_SHARED_LIBRARY)
```
