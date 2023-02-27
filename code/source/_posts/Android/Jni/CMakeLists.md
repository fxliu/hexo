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

## 示例

* 最简实例

```makefile
cmake_minimum_required(VERSION 3.0)
project(HELLO VERSION 1.0 LANGUAGES C CXX)
set(SOURCES main.c)
add_executable(hello ${SOURCES})
```

* lib示例

```makefile
# 先将 hello.c 生成一个中间库hellolib，再链接到main.c
cmake_minimum_required(VERSION 3.0)
project(HELLO VERSION 1.0 LANGUAGES C CXX)

set(LIB_SRC hello.c)
add_library(libhello ${LIB_SRC})

set(APP_SRC main.c)
add_executable(hello ${APP_SRC})

target_link_libraries(hello libhello)
```

* 常用

```makefile
cmake_minimum_required(VERSION 3.18.1)
project("lib***")
# 隐藏符号
set(CMAKE_C_VISIBILITY_PRESET hidden)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
# 打印日志
MESSAGE([SEND_ERROR | STATUS | FATAL_ERROR] "message to display" ...)
# SEND_ERROR 产生错误，生成过程被跳过
# STATUS 输出前缀为—(杠)的信息
# FATAL_ERROR 立即终止所有 cmake 过程
message(STATUS "PROJECT_NAME: " ${PROJECT_NAME})
```

## 基础使用

* 版本号约束

```makefile
# 设置cmake最低版本
cmake_minimum_required(VERSION 3.2)
```

* 全局变量

```makefile
# 当前makefile路径
${CMAKE_CURRENT_SOURCE_DIR}
# 最外层CMakeLists.txt所在目录
${CMAKE_SOURCE_DIR}
# ABI
${CMAKE_ANDROID_ARCH_ABI}

# 当前操作系统

```

* 工具函数

```makefile
# 打印消息
message(消息)
```

* 工程属性

```makefile
# project命令用于指定cmake工程的名称, 还可以指定cmake工程的版本号（VERSION关键字）、简短的描述（DESCRIPTION关键字）、主页URL（HOMEPAGE_URL关键字）和编译工程使用的语言（LANGUAGES关键字）
# project(<PROJECT-NAME> [<language-name>...])
# project(<PROJECT-NAME> [VERSION <major>[.<minor>[.<patch>[.<tweak>]]]] [DESCRIPTION <project-description-string>][HOMEPAGE_URL <url-string>] [LANGUAGES <language-name>...])
# ${PROJECT_SOURCE_DIR} 和 <PROJECT-NAME>_SOURCE_DIR：本CMakeLists.txt所在的文件夹路径
# ${PROJECT_NAME}：本CMakeLists.txt的project名称
project(xxx)
project(mytest VERSION 1.2.3.4)
project(mytest HOMEPAGE_URL “https://www.XXX(示例).com”)

# 设置编译选项及默认值
option(TEST_DEBUG "option for debug" OFF)
```

* 宏定义

```makefile
# 宏编译
if (MSVC)
        ...
else()
        ...
endif()
# 非宏编译
if (NOT DEFINED BUILD_WRITERS)
        ...
endif()

# 添加编译选项FOO BAR
# add_definitions定义宏，但是这种定义方式无法给宏具体值 
# #define  MG_ENABLE_OPENSSL
add_definitions(-DFOO -DBAR ...)

# add_compile_definitions定义宏，这种方式可以给宏具体值，但是这个指令只要高版本的cmake支持
# #define  MG_ENABLE_OPENSSL   1 
add_compile_definitions(MG_ENABLE_OPENSSL=1)
```

* 变量

```makefile
# 给文件名/路径名或其他字符串起别名，用${变量}获取变量内容
set(变量 文件名/路径/...)

# 隐藏符号 - 系统变量
set(CMAKE_C_VISIBILITY_PRESET hidden)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)

# 获取路径下所有的.cpp/.c/.cc文件（不包括子目录），并赋值给变量中
aux_source_directory(路径 变量)

# GLOB 获取目录下的所有cpp文件（不包括子目录），并赋值给SOURCES
file(
        GLOB SOURCES
        ${PROJECT_SOURCE_DIR}/*.c
)
# GLOB_RECURSE 获取目录下的所有cpp文件（包括子目录），并赋值给NATIVE_SRC
file(
        GLOB_RECURSE NATIVE_SRC 
        ${PROJECT_SOURCE_DIR}/lib/*.cpp
)
```

* 添加头文件目录

```makefile
include_directories(路径)

include_directories(
        ./include
        ./
)
```

* 目标生成

```makefile
# 设置.so/.a库文件生成路径
link_directories(路径)

# 设置可执行文件输出路径
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
# 设置lib库输出路径
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)

# 将.cpp/.c/.cc文件生成.a静态库
# 注意，库文件名称通常为libxxx.so，在这里只要写xxx即可
# 库的源文件可指定，也可用target_sources()后续指定
add_library(库文件名称 STATIC 文件)

# 将.cpp/.c/.cc文件生成可执行文件
add_executable(可执行文件名称 文件)

# 目标属性重命名
set_target_properties(libhello PROPERTIES OUTPUT_NAME "hello")
set_target_properties(Thirdlib PROPERTIES IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/jniLibs/libThirdlib.so)
set_target_properties(test PROPERTIES LINKER_LANGUAGE CXX)      # 指定C++
set_target_properties(test PROPERTIES LINKER_LANGUAGE C)        # 指定C

# 对 add_library 或 add_executable 生成的文件进行链接操作
# 注意，库文件名称通常为libxxx.so，在这里只要写xxx即可
target_link_libraries(库文件名称/可执行文件名称 链接的库文件名称)
```

* 多层嵌套

```makefile
# 添加一个子目录并构建该子目录, add_subdirectory本质上引入指定目录的CMakefile
# 相互引用/嵌套, 还是单纯的多个目标生成 都可以
add_subdirectory(./libusb)

# binary_dir 该参数指定一个目录，用于存放输出文件
# EXCLUDE_FROM_ALL 当指定了该参数，除非父目录明确包含, 否则则子目录下的目标不会被父目录下的目标文件包含进去
add_subdirectory (source_dir [binary_dir] [EXCLUDE_FROM_ALL])
```

* 库引入实例

```makefile
# 系统库引入
find_library(
        # Sets the name of the path variable.
        log-lib

        # Specifies the name of the NDK library that
        # you want CMake to locate.
        log
)
# 第三方库引入 - 静态库
# 指定 IMPORTED, 直接导入已经生成的库, cmake不会给这类library添加编译规则
# 并设置 IMPORTED_LOCATION 属性, 指定库路径
set(OpenSSL_DIR ${CMAKE_SOURCE_DIR}/libs)
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
# 区分Debug和Release写法
add_library(baz STATIC IMPORTED)
set_target_properties(baz PROPERTIES
IMPORTED_LOCATION_RELEASE ${CMAKE_CURRENT_SOURCE_DIR}/libbaz.a
IMPORTED_LOCATION_DEBUG ${CMAKE_CURRENT_SOURCE_DIR}/libbazd.a)
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
# 添加别名: add_library(<name> ALIAS <target>)
```

```makefile
# android jni工程挂载
# opencv
set(OpenCV_DIR ${CMAKE_SOURCE_DIR}/OpenCV-android-sdk/sdk/native/jni/abi-${CMAKE_ANDROID_ARCH_ABI})
find_package(OpenCV REQUIRED)

target_link_libraries(
        ...
        ${OpenCV_LIBS}
        ...
)
```

```makefile
# 动态so加载
# rga
set(RGA_LIB ${CMAKE_SOURCE_DIR}/libs/${CMAKE_ANDROID_ARCH_ABI}/librga.so)
include_directories(${CMAKE_SOURCE_DIR}/rga/include)

# opencv
set(OPENCV_LIB ${CMAKE_SOURCE_DIR}/libs/${CMAKE_ANDROID_ARCH_ABI}/libopencv_java4.so)
include_directories(${CMAKE_SOURCE_DIR}/opencv/native/jni/include)

target_link_libraries(
        ...
        ${RGA_LIB}
        ${OPENCV_LIB}
        ...
)
```
