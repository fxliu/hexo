---
title: CMakeLists
tags: 
    - CMakeLists
categories: 
    - Android
description: CMakeLists
date: 2022-03-20 17:12:48
updated: 2022-03-20 17:12:48
---

## 配置

```gradle
```

## 基础使用

```makefile
add_library(
        # Sets the name of the library.
        lib_***_sdk

        # Sets the library as a shared library.
        # SHARED
        STATIC

        # Provides a relative path to your source file(s).
        # Json
        json/json_value.cpp
        json/json_reader.cpp
        json/json_writer.cpp

        # lib_eidnfs_sdk
        lib_***_sdk.cpp
)
# include
include_directories(
        ./include
        ./
)
# 系统库引入
find_library(
        # Sets the name of the path variable.
        log-lib

        # Specifies the name of the NDK library that
        # you want CMake to locate.
        log
)
# 第三方库引入
set(OpenSSL_DIR ${CMAKE_SOURCE_DIR}/libs)
#这里引用静态.a, ssl,crypto
add_library(crypto STATIC IMPORTED)
add_library(ssl STATIC IMPORTED)
# 这里加载，并且找到相应的 libxxx.a
set_target_properties( # Specifies the target library.
        crypto
        # Specifies the parameter you want to define.
        PROPERTIES IMPORTED_LOCATION
        # Provides the path to the library you want to import.
        ${OpenSSL_DIR}/${ANDROID_ABI}/libcrypto.a )
set_target_properties( # Specifies the target library.
        ssl
        # Specifies the parameter you want to define.
        PROPERTIES IMPORTED_LOCATION
        # Provides the path to the library you want to import.
        ${OpenSSL_DIR}/${ANDROID_ABI}/libssl.a )
# 链接
target_link_libraries(
        # Specifies the target library.
        lib_eidnfs_sdk

        # Links the target library to the log library
        # included in the NDK.
        ssl
        crypto
        ${log-lib}
)
```
