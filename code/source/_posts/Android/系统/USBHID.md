---
title: USBHID
tags: 
  - USBHID
  - libusb
categories: 
  - Android
description: USBHID, libusb
date: 2020-09-26 16:56:17
updated: 2020-09-26 16:56:17
---

## DEMO

[UsbManager](es:svn\bar_machine\trunk\C++\EIDSDK\Android\EsEidDemo)
[lib_eididcard_sdk](\svn\eidcard\trunk\Android\EidIDCardSdkDemo)
[android_mk](https://developer.android.google.cn/ndk/guides/android_mk)

## libusb

[案例1](https://www.cnblogs.com/yongdaimi/p/11934783.html)
[案例2](https://www.dazhuanlan.com/2019/10/02/5d945baad2be9/)

+ 下载[libusb](https://libusb.info/), [github](https://github.com/libusb/libusb/releases)
+ 测试案例版本：`libusb-1.0.23`
+ 在`app/src/main`目录下新建: `jni/libusb-1.0.23`
  + 复制 `libusb-1.0.23/libusb` -> `jni/libusb-1.0.23/libusb`
  + 复制 `libusb-1.0.23/android/config.h` -> `jni/libusb-1.0.23/config.h`
  + 复制 `libusb-1.0.23/android/libusb.mk` -> `jni/libusb-1.0.23/libusb.mk`
  + 复制 `libusb-1.0.23/android/Android.mk` -> `jni/libusb-1.0.23/Android.mk`
+ 修改 Android.mk，屏蔽案例和测试

```makefile
include $(LOCAL_PATH)/libusb.mk
# include $(LOCAL_PATH)/examples.mk
# include $(LOCAL_PATH)/tests.mk
```

+ **打开app目录下的build.gradle文件，指定JNI目录**

```gradle
android {
    compileSdkVersion 29
    buildToolsVersion "30.0.2"

    defaultConfig {
        // ...
    }

    sourceSets {
        main {
            // 指定JNI目录
            jniLibs.srcDirs = ['src/main/jni']
        }
    }
}
```

+ **创建文件：jni/Android.mk**

```makefile
#
# Copyright (c) 2019 Realsil.Inc. All rights reserved.
#
include $(call all-subdir-makefiles)
```

```makefile
LOCAL_PATH:= $(call my-dir)

include $(LOCAL_PATH)/libsdk.mk
include $(LOCAL_PATH)/libtest.mk
```

+ **创建文件：jni/Application.mk**

```makefile
#
# Copyright (c) 2019 SEP.Inc. All rights reserved.
#

APP_ABI := all
# APP_ABI := armeabi, armeabi-v7a, x86, mips, arm64-v8a, mips64, x86_64

APP_LDFLAGS := -llog
```

+ **修改libusb.mk, 更新当前源代码的位置**

```makefile
# 把各个地方的 ..\ 去掉
LOCAL_PATH:= $(call my-dir)
LIBUSB_ROOT_REL:= .
LIBUSB_ROOT_ABS:= $(LOCAL_PATH)

# libusb

include $(CLEAR_VARS)

LIBUSB_ROOT_REL:= .
LIBUSB_ROOT_ABS:= $(LOCAL_PATH)

LOCAL_SRC_FILES := \
  $(LIBUSB_ROOT_REL)/libusb/core.c \
  $(LIBUSB_ROOT_REL)/libusb/descriptor.c \
  $(LIBUSB_ROOT_REL)/libusb/hotplug.c \
  $(LIBUSB_ROOT_REL)/libusb/io.c \
  $(LIBUSB_ROOT_REL)/libusb/sync.c \
  $(LIBUSB_ROOT_REL)/libusb/strerror.c \
  $(LIBUSB_ROOT_REL)/libusb/os/linux_usbfs.c \
  $(LIBUSB_ROOT_REL)/libusb/os/poll_posix.c \
  $(LIBUSB_ROOT_REL)/libusb/os/threads_posix.c \
  $(LIBUSB_ROOT_REL)/libusb/os/linux_netlink.c

LOCAL_C_INCLUDES += \
  $(LOCAL_PATH) \
  $(LIBUSB_ROOT_ABS)/libusb \
  $(LIBUSB_ROOT_ABS)/libusb/os

LOCAL_EXPORT_C_INCLUDES := \
  $(LIBUSB_ROOT_ABS)/libusb

LOCAL_LDLIBS := -llog

LOCAL_MODULE := libusb1.0

include $(BUILD_SHARED_LIBRARY)
```

+ **任意文件夹下右击，选择`Link C++ Project with Gradle`**
  + 在`Build System`的下拉列表中选择`ndk-build`的编译方式
  + 指定所有模块的`makefile`文件位置: `jni/Android.mk`
  + 点OK， 此时编译系统就会自动开始构建，注意到此时文件夹的目录颜色已修改，且app目录下的`build.gradle`文件也进行了更新

```gradle
android {
    // ...
    sourceSets {
        main {
            // 指定JNI目录
            jniLibs.srcDirs = ['src/main/jni']
        }
    }
    externalNativeBuild {
        ndkBuild {
            path file('src/main/jni/Android.mk')
        }
    }
}
```

### libusb 配置

```h
// 默认已包含：ANDROID 系统标记
#ifndef __ANDROID__
#define __ANDROID__
#endif

// 异常日志：默认开
#define ENABLE_LOGGING
// 详细日志：默认关
#define ENABLE_DEBUG_LOGGING
```
