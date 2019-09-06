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

### 备记几个FFmepg常用参数

+ 格式转换
  + `ffmpeg -i input.avi output.mp4`
  + `-vcodec mpeg4`：指定编码格式
+ 裁剪：从30秒开始到40秒
  + `ffmpeg -i input.wmv -ss 30 -t 10 output.wmv`
  + `ffmpeg -i input.wmv -ss 30 -to 40 output.wmv`
  + `-c copy`：复制所有的流
  + `-vcodec copy`：使用跟原视频一样的视频编解码器
  + `-acodec copy`：使用跟原视频一样的音频编解码器
+ 音量：音贝
  + `.\ffmpeg -i s1.mp4 -af "volumedetect" -f null /dev/null`：查看`mean_volume`->`max_volume`
  + `ffmpeg  -i input.mp3 -af "volume=0.5" output.mp3`：减半
  + `ffmpeg  -i input.mp3 -af "volume=2" output.mp3`：加倍
  + `ffmpeg  -i input.mp3 -af "volume=5dB" output.mp3`：增加指定分贝数（使用负数`-5dB`则为降低分贝）
  + `ffmepg -i input.mp3 -filter:a "loudnorm" output.mp3`：音频标准化：削峰填谷，使整个音频的音量变化跨度降低，变得平滑

## SDL环境(2.0)

+ [SDL官网](http://www.libsdl.org/)

### SDL引入

```C++
extern "C"
{
#include "ffmpeg\libavutil\frame.h"
#include "SDL/SDL.h"
};
#pragma comment(lib, "SDL2.lib")
```

### SDL应用

```C++
// 初始化
SDL_Init(SDL_INIT_EVERYTHING);
// 创建窗体：支持直接创建一个弹出窗，或者附加到指定窗体句柄上
if (!m_hWnd)
{
  m_sdlWindow = SDL_CreateWindow("SDL_Window", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
    w, h, SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE);
}
else {
  m_sdlWindow = SDL_CreateWindowFrom(m_hWnd);
}
// 渲染器
m_sdlRenderer = SDL_CreateRenderer(m_sdlWindow, -1, 0);
// 设置Renderer按视频比例(m_videoWidth, m_videoHeight)缩放，默认按屏幕拉伸
SDL_RenderSetLogicalSize(m_sdlRenderer, m_videoWidth, m_videoHeight);
// 纹理：Texture宽高一定要对应视频宽高
m_sdlTexture = SDL_CreateTexture(m_sdlRenderer, SDL_PIXELFORMAT_IYUV, SDL_TEXTUREACCESS_STREAMING, m_videoWidth, m_videoHeight);

// 视频播放 frame 为FFmepg解码后的数据帧
if (m_sdlTexture) SDL_UpdateTexture(m_sdlTexture, NULL, frame->data[0], frame->linesize[0]);
// 遇到SDL_UpdateTexture崩溃情况的话，可以尝试直接调用SDL_UpdateYUVTexture
//if (m_sdlTexture) SDL_UpdateYUVTexture(m_sdlTexture, NULL,
//  frame->data[0], frame->linesize[0], frame->data[1], frame->linesize[1], frame->data[2], frame->linesize[2]);
if (m_sdlRenderer) SDL_RenderClear(m_sdlRenderer);
if (m_sdlRenderer && m_sdlTexture) SDL_RenderCopy(m_sdlRenderer, m_sdlTexture, NULL, NULL);
if (m_sdlRenderer) SDL_RenderPresent(m_sdlRenderer);

// 清理
if (m_sdlTexture)
{
  SDL_DestroyTexture(m_sdlTexture);
  m_sdlTexture = NULL;
}
if (m_sdlRenderer)
{
  SDL_DestroyRenderer(m_sdlRenderer);
  m_sdlRenderer = NULL;
}
if (m_sdlWindowScreen)
{
  SDL_FreeSurface(m_sdlWindowScreen);
  m_sdlWindowScreen = NULL;
}
if (m_sdlWindow)
{
  SDL_DestroyWindow(m_sdlWindow);
  m_sdlWindow = NULL;
}
SDL_Quit();
// ----------------------------------------------------------
// 音频播放回调
//音频设备需要更多数据的时候会调用该回调函数
void CMyVideo::read_audio_data(void *udata, Uint8 *stream, int len)
{
  CMyVideo *pThis = (CMyVideo*)udata;
  //首先使用SDL_memset()将stream中的数据设置为0
  SDL_memset(stream, 0, len);
  if (pThis->m_audio_len == 0)
    return;
  len = (len > (int)pThis->m_audio_len ? pThis->m_audio_len : len);
  // 最后一个参数代表音量：SDL_MIX_MAXVOLUME
  SDL_MixAudio(stream, pThis->m_audio_pos, len, pThis->m_volume);
  pThis->m_audio_pos += len;
  pThis->m_audio_len -= len;
}
// 打开音频
BOOL CMyVideo::OpenAudio(int audioRate, Uint16 audioFrameSize)
{
  // 音频参数: 最好和视频参数保持一致，否则会有杂声
  SDL_AudioSpec spec;
  spec.freq = audioRate;        // 对应音频转换设置
  spec.format = AUDIO_S32;      // 对应音频转换设置
  spec.channels = 2;
  spec.silence = 0;
  spec.samples = audioFrameSize;    // 对应音频帧缓存大小
  spec.callback = read_audio_data;
  spec.userdata = this;

  if (SDL_OpenAudio(&spec, NULL) < 0)
  {
    return FALSE;
  }
  SDL_PauseAudio(0);
  return TRUE;
}
// 音频播放：buf/len为FFmepg音频解析结果
m_audio_chunk = buf[0];
m_audio_pos = m_audio_chunk;
m_audio_len = len;
// 等待播放完成
while (m_audio_len > 0)
  SDL_Delay(1);

// 音频关闭
SDL_CloseAudio();
```

## SDL扩展

+ [SDL_Image](http://www.libsdl.org/projects/SDL_image/)扩展支持多种类型图片加载
  + SDL默认只支持加载BMP
+ [SDL_mixer](http://www.libsdl.org/projects/SDL_mixer/)扩展各种音乐播放

```C++
// 窗体创建：略，SDL窗体句柄：sdlWindow
SDL_Surface *image = SDL_LoadBMP("1.bmp");
SDL_Renderer *renderer = SDL_CreateRenderer(sdlWindow, -1, 0);
SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, image);
// SDL_RenderClear(renderer);
// 复制到渲染器
SDL_RenderCopy(renderer, texture, NULL, NULL);
// 渲染显示
SDL_RenderPresent(renderer);
// 数据释放：略
```

```C++
// 代码备记：未校验
#include<SDL\SDL_mixer.h>
SDL_Init(SDL_INIT_EVERYTHING)
Mix_OpenAudio(44100,MIX_DEFAULT_FORMAT,2,2048);
Mix_Music *sound=Mix_LoadMUS("sound.wav");
Mix_PlayMusic(sound,1);
```

## 备注

+ 注意FFmepg解析和SDL播放需要多线程分开，避免视频/音频播放卡顿
+ SDL音频和视频的播放一定要多线程，不能相互等待
+ 音频和视频要注意延迟处理，Window延迟控制是达不到播放要求的，做个毫秒级的延迟同步即可，人类是感知不到这点误差的
+ 音视频同步要控制视频播放，让视频帧根据音频播放加减速，声音播放不能卡顿，很容被人耳感知的
+ SDL核心是图像的加载，渲染，显示；而视频播放就是图片快速切换而已。

## Demo

[FFmpeg+SDL播放器](https://github.com/fxliu/VCDemo/tree/master/TOOLS/ffmpeg+SDL)
`https://github.com/fxliu/VCDemo/tree/master/TOOLS/ffmpeg+SDL`
