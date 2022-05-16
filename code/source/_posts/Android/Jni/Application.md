---
title: Application
tags: 
    - Application
categories: 
    - Android
description: Application
date: 2022-03-20 16:23:01
updated: 2022-03-20 16:23:01
---

## 基础应用

```makefile
# 指定ABI
APP_ABI := armeabi-v7a, arm64-v8a
# APP_ABI := all
# APP_ABI := armeabi, armeabi-v7a, x86, mips, arm64-v8a, mips64, x86_64

# 编译参数
APP_LDFLAGS := -llog
APP_CPPFLAGS += -fexceptions -frtti

# 依赖环境
APP_STL := c++_shared

```

## ndk 直接编译 so

```makefile
# Android.mk
# ----------
# 每个Android.mk 文件都必须已LOCAL_PATH开始，my-dir返回包含Android.mk的路径
LOCAL_PATH:= $(call my-dir)

# 负责清理一些Local_XXX，但不清理LOCAL_PATH，这个清理动作是必须的
include $(CLEAR_VARS)

# 模块名，不能有空格，自动生成：lib***.so
LOCAL_MODULE := wlt

# 编译参数：只导出指定函数，内联函数默认隐藏
LOCAL_CFLAGS += -fvisibility-inlines-hidden -fvisibility=hidden -fno-common
LOCAL_CPPFLAGS += -std=c++11 -fvisibility-inlines-hidden -fvisibility=hidden -fno-common

# 源文件
LOCAL_SRC_FILES := EsWlt.cpp

# 表示动态编译库，也就是生成so
include $(BUILD_SHARED_LIBRARY)

```

```makefile
# Application.mk
# ----------
# NDK库版本号，对应 build.gradle minSdk配置
APP_PLATFORM := android-21

# 目标平台
APP_ABI := armeabi-v7a, arm64-v8a
# APP_ABI := all
# APP_ABI := armeabi, armeabi-v7a, x86, mips, arm64-v8a, mips64, x86_64

# Android日志库
# APP_LDFLAGS := -llog

# 启用异常处理
APP_CPPFLAGS += -fexceptions
# rtti特性即 (running time type identification) 运行时鉴别对象类型的能力
APP_CPPFLAGS += -frtti

# 如何链接C++标准库，c++_static表示静态链接，c++_shared 表示动态链接
APP_STL := c++_static
```

```bat
:: build.mk
:: ----------
:: 必须放置于 jni 目录下，否则编译报错
:: NDK 路径
@set path=%path%;D:\Android\Sdk\ndk\23.1.7779620
:: 编译
@call ndk-build clean
@call ndk-build

pause
```
