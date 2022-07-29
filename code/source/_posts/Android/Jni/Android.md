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

# mongoose
LOCAL_SRC_FILES += \
  $(LIBUSB_ROOT_REL)/mongoose/mongoose.c

# include
LOCAL_C_INCLUDES += \
  $(LOCAL_PATH) \
  $(LIBUSB_ROOT_ABS)/mongoose \

LOCAL_EXPORT_C_INCLUDES := \
  $(LIBUSB_ROOT_ABS)/libusb \
  $(LIBUSB_ROOT_ABS)/openssl
# 编译参数
LOCAL_CFLAGS := -pthread
# 系统库
LOCAL_LDLIBS := -llog
# 第三方静态库
LOCAL_STATIC_LIBRARIES := ssl crypto
# 目标名称
LOCAL_MODULE := lib_eididcard_sdk
include $(BUILD_SHARED_LIBRARY)
```

```makefile
# so：仅参与编译，并不打包该so文件，避免多aar包含相同文件导致冲突
LOCAL_C_INCLUDES += ${LOCAL_PATH}/../../../../opencv/native/jni/include/
LOCAL_LDLIBS += -L${LOCAL_PATH}/../../../../opencv/native/libs/$(TARGET_ARCH_ABI)/ -lopencv_java4 -lomp
```

```makefile
# so
include $(CLEAR_VARS)
LOCAL_MODULE := ts-prebuilt
LOCAL_SRC_FILES := ${LOCAL_PATH}/../../../libs/$(TARGET_ARCH_ABI)/libtennis.so
LOCAL_EXPORT_C_INCLUDES := ${LOCAL_PATH}/SeetaFace6/TenniS/include/
include $(PREBUILT_SHARED_LIBRARY)

LOCAL_SHARED_LIBRARIES += ts-prebuilt
```
