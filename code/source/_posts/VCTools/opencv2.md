---
title: opencv2
tags: 
  - opencv
categories: 
  - VC
description: opencv
date: 2019-09-07 16:51:20
updated: 2019-09-07 16:51:20
---

## opencv2部署

+ [官网](https://opencv.org/releases/)
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

### opencv2

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

### opencv2 Demo

[opencv2 Demo](https://github.com/fxliu/VCDemo/tree/master/TOOLS/opencv)
`https://github.com/fxliu/VCDemo/tree/master/TOOLS/opencv`

## opencv4.6 编译

+ [官网](https://opencv.org/releases/)
  + 下载中文安装包即可, 安装后就有源码了
  + 下载对应版本的[opencv_contrib](https://github.com/opencv/opencv_contrib/tree/4.6.0)
  + 下载最新版本[cmake](https://cmake.org/download/)
+ 编译
  + 启动cmake-gui
  + Browse Source -> D:\opencv\sources
  + Browse Build -> D:\opencv\build
  + configure
    + 选择VS编译环境
  + search OPENCV_EXTRA_MODULES_PATH -> 选择为opencv_contrib目录中的modules目录
    + 注意目录字符是/，不要Windows复制粘贴路径，点击目录选择按钮去选择路径
  + 再次configure
  + 点击Generate生成
  + 在build即可找到VS工程文件

## 轮廓获取/比对

```c++
// 二值化
threshold(mat, mat, 127, 255, cv::THRESH_BINARY_INV);
// 提取轮廓 - 一系列坐标点
std::vector<std::vector<cv::Point>> curContours;
// 轮廓从属关系
std::vector<cv::Vec4i> dstHierarchy;
findContours(mat, curContours, dstHierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE, cv::Point(0, 0));
for(int idx = 0; idx < curContours.size(); idx++) {
    std::vector<cv::Point> &dstContour1 = curContours[idx];
    if(dstContour1.size() > 5) {
        SDK_LOGE("--------------------------------------------------------");
        for(int subIdx = 0; subIdx < dstContour1.size(); subIdx++)
            SDK_LOGE("dstContour1: %d, %d", dstContour1[subIdx].x, dstContour1[subIdx].y);
        SDK_LOGE("--------------------------------------------------------");
        lastContours.push_back(dstContour1);
    }
}
// 轮廓相似度
threshold(mat, mat, 127, 255, cv::THRESH_BINARY_INV);
std::vector<std::vector<cv::Point>> dstContours2;
std::vector<cv::Vec4i> dstHierarchy;
findContours(mat, dstContours2, dstHierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE, cv::Point(0, 0));

int findIdx = 0;
for(int idx = 0; idx < lastContours.size(); idx++) {
    std::vector<cv::Point> &dstContour1 = lastContours[idx];
    for(int subIdx = 0; subIdx < dstContours2.size(); subIdx++) {
        std::vector<cv::Point> &dstContour2 = dstContours2[subIdx];
        double gSimilarity = matchShapes(dstContour1, dstContour2, cv::CONTOURS_MATCH_I3, 0);
        if(gSimilarity < 0.2) {
            SDK_LOGE("dstContour: idx = %d, v = %f", idx, gSimilarity);
            findIdx += 1;
        }
    }
}
```
