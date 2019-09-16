---
title: opencv2
tags: 
  - opencv
categories: 
  - VC
---

## opencv2部署

+ 官网下载windows安装包：2.x版支持x86，3以上只有x64
+ 案例：opencv-2.4.13.6-vc14.exe
  + build\include
  + build\include\x86\vc14\staticlib：静态lib
  + build\include\x86\vc14\lib + bin：动态lib + dll

### 引入

```C++
// 基础lib - release版去掉文件名最后面的"d"
#pragma comment(lib, "IlmImfd.lib")
#pragma comment(lib, "libjasperd.lib")
#pragma comment(lib, "libjpegd.lib")
#pragma comment(lib, "libpngd.lib")
#pragma comment(lib, "libtiffd.lib")
#pragma comment(lib, "zlibd.lib")
// 功能lib，根据代码需要补充
#pragma comment(lib, "opencv_core2413d.lib")
#pragma comment(lib, "opencv_highgui2413d.lib")
#pragma comment(lib, "opencv_imgproc2413d.lib")
// 静态lib需要补充下面几个
#pragma comment(lib, "vfw32.lib")
#pragma comment(lib, "comctl32.lib")
#pragma comment(lib, "gdi32.lib")
```

### 简单应用

```C++
VideoCapture cap(0);
if (!cap.isOpened())
{
  // 尝试打开另一个摄像头
  if (!cap.open(1))
    return 0;
}
// 设置摄像头参数: 这个要根据摄像头支持参数设置
cap.set(CV_CAP_PROP_FRAME_WIDTH, 640);
cap.set(CV_CAP_PROP_FRAME_HEIGHT, 480);
cap.set(CV_CAP_PROP_FPS, 30);
// 检查设置是否生效
int width = (int)cap.get(CV_CAP_PROP_FRAME_WIDTH);
int height = (int)cap.get(CV_CAP_PROP_FRAME_HEIGHT);
if (width != 640 || height != 480)
  return 0;

Mat frame;
// 窗体命名
char* title = "摄像头";
cvNamedWindow(title, WINDOW_NORMAL);
// 设置全屏
//cvSetWindowProperty(title, CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
while (cap.isOpened())
{
  //cap >> frame;
  if (!cap.read(frame))
    break;
  if (frame.empty())
    break;
  imshow(title, frame);
  char ch = waitKey(30);
}
```

## Demo

[opencv2 Demo](https://github.com/fxliu/VCDemo/tree/master/TOOLS/opencv)
`https://github.com/fxliu/VCDemo/tree/master/TOOLS/opencv`
