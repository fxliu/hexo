---
title: FFmepg(4.2)+SDL(2.0)播放器
tags: 
  - FFmepg
  - SDL 
categories: 
  - 博客
---

## FFmepg环境(4.2)

+ [FFmepg官网](http://ffmpeg.zeranoe.com/builds/) 下载最新的ffmpeg的dev版和share版，当前最新版是4.2
  + 注意区分x64和x86，取决于你vs2015调试的解决方案平台用什么，如果安装了错误的版本将会出现一堆无法解析的错误
  + 包含三个版本：Static、Shared以及Dev
    + Static: 包含3个应用程序：ffmpeg.exe , ffplay.exe , ffprobe.exe，体积都很大，相关的DLL已经被编译到exe里面去了。
    + Shared: 除了ffmpeg.exe , ffplay.exe , ffprobe.exe之外还有一些DLL，exe体积很小，在运行时到相应的DLL中调用功能。
    + Dev: 开发者（developer）版本，里面包含了库文件xxx.lib以及头文件xxx.h，这个版本不含exe文件
  + 把dev版本与share版本都下下来解压，dev版本文件夹中的Include和lib目录整个儿复制到VS项目目录下
  + 将share版本文件夹中bin目录下对应的所有dll复制到exe根目录

### FFmepg引入

```C++
// 头文件中的函数定义在编译为 C 程序的文件中，而头文件是在 C++ 文件中不带 extern “C” 修饰符声明的。在此情况下，需要添加extern "C"修饰符。
// 不添加 extern “C” 修饰符 会提示 无法解析 导致编译失败
extern "C"
{
#include "libavcodec\avcodec.h"  
#include "libavformat\avformat.h"  
#include "libavutil\channel_layout.h"  
#include "libavutil\common.h"  
#include "libavutil\imgutils.h"  
#include "libswscale\swscale.h"
#include "libavutil\imgutils.h"
#include "libavutil\opt.h"
#include "libavutil\mathematics.h"
#include "libavutil\samplefmt.h"
};

#pragma comment(lib, "avcodec.lib")
#pragma comment(lib, "avformat.lib")
#pragma comment(lib, "avdevice.lib")
#pragma comment(lib, "avfilter.lib")
#pragma comment(lib, "avutil.lib")
#pragma comment(lib, "postproc.lib")
#pragma comment(lib, "swresample.lib")
#pragma comment(lib, "swscale.lib")
// 测试
printf("%s", avcodec_configuration());
```

### FFmepg应用

关键函数调试不通过时，还是自己到dev版的examples搜函数使用案例吧，网上各种旧版本的说明，有些函数已经废弃了，调用逻辑也不对

视频播放基本上时固定模式打开->参数设定->读取->解码->转码->显示，剩下的看Demo吧

音频处理流程基本类似

+ `avformat_open_input`打开视频文件
  + `avformat_close_input`关闭视频文件
+ `av_read_frame`读
+ `avcodec_send_packet` -> `avcodec_receive_frame`解码
+ `sws_scale`转码，Demo中时转为YUV420P格式，提供SDL播放
  + 注意保存解码结果的缓冲区的申请，被网上旧代码各种坑，自己去examples看官方势力吧
  + 注意还有个视频/音频播放延迟提取，SDL播放时要做到音视频同步

## SDL环境(2.0)

+ [SDL官网](http://www.libsdl.org/)

### SDL引入

```C++
// TODO: 待补充
```

### SDL应用

```C++
// TODO: 待补充
```

## Demo

[FFmpeg+SDL播放器](https://github.com/fxliu/VCDemo/tree/master/TOOLS/ffmpeg+SDL)
`https://github.com/fxliu/VCDemo/tree/master/TOOLS/ffmpeg+SDL`
