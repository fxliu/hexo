---
title: opencv
tags: 
    - opencv
categories: 
    - Android
description: opencv
date: 2022-07-23 00:22:28
updated: 2022-07-23 00:22:28
---

## Android-SDK

* [SDK](https://opencv.org/releases/)

```sh
# 正常使用直接从 https://opencv.org/releases/ 下载Android-SDK即可
# 示例为: 自编译扩展 opencv_contrib 使用
# opencv-4.6.0 + opencv_contrib-4.6.0

# Java环境
# AndroidStudio默认Java路径 有可能只是一个mark标记, 需要重新配置系统环境JAVA_HOME为有效路径
# JAVA_HOME: D:\Program Files\Java\jdk1.8.0_261

# 命令行执行根目录: opencv-4.6.0 根目录
mkdir build
# 注意最后面尾缀两个路径: [work_dir] [opencv_dir]
# 编译的命令可以加上–no_ccache，不过不加也不会怎样，就是会报错，但程序还是可以正常进行下去
python2 .\platforms\android\build_sdk.py --config .\platforms\android\ndk-22.config.py --sdk_path D:\Android\Sdk --ndk_path D:\Android\Sdk\ndk\25.0.8775105 --no_ccache --no_samples_build .\build .\
# 扩展opencv_contrib参数
python2 .\platforms\android\build_sdk.py --config .\platforms\android\ndk-22.config.py --sdk_path D:\Android\Sdk --ndk_path D:\Android\Sdk\ndk\25.0.8775105 --extra_modules_path ..\opencv_contrib-4.6.0\modules --no_ccache --no_samples_build .\build .\

# 编译完成最后会输出SDK生成目录
SDK location: .\build\OpenCV-android-sdk
Documentation .\build\OpenCV-android-sdk\sdk\java\javadoc

# build_sdk.py 只是帮助生成cmake等相关命令行, 并执行
# 可以自行从对应位置 拦截打印 命令行保留使用

# modules目录中, 每个子目录对应一个模块
# 模块选择: 禁用指定模块, 自动禁用依赖被禁模块的所有模块
-DBUILD_opencv_calib3d=OFF
# 模块选择: 只编译编译指定模块, 和它们依赖的所有模块
-DBUILD_LIST=calib3d,videoio,ts
# 可以修改 build_sdk.py Builder::build_library函数cmake_vars默认值, 禁用模块
# 编译命令要加上--no_samples_build, 否则samples编译失败会报错终端编译过程
cmake_vars = dict(
    # 增加一下内容
    BUILD_LIST="core,imgcodecs,imgproc,java,photo,stitching,world",
    #BUILD_LIST="core,imgcodecs,imgproc,java,photo,stitching,world,dnn_superres",
)
```

| 模块       | 功能                                | 备注   |
| ---------- | ----------------------------------- | ------ |
| calib3d    | 3D重建模块, 摄像机标定              |      |
| core       | 核心模块，包含最基础的操作          |       |
| dnn        | 深度神经网络模块                    |        |
| features2d | 2D特征检测模块                      |        |
| flann      | 最近邻搜索模块-多维空间的聚类与搜索 |        |
| gapi       | Graph API，pipeline引擎，用来加速图像处理 |        |
| highgui    | 高层图像用户界面                    |        |
| imgcodecs  | 类型转换, 主要用于文件读写          |        |
| imgproc    | 图像处理模块                        |        |
| java       |                                     |        |
| js         |                                     |        |
| ml         | 机器学习模块                        |        |
| objc       |                                     |        |
| objdetect  | 目标检测模块                        |        |
| photo      | 计算图像学,包含图像修复和去噪等功能   |        |
| python     |                                     |        |
| stitching  | 图像拼接模块                        |        |
| ts         | 测试库，用于单元测试                 |        |
| video      | 视频处理模块                        |        |
| videoio    | 视频I/O                             |        |
| world      | 将所有模块的库文件合并成一个大的库文件 | 必要 |

| opencv_contrib | 功能                                | 备注   |
| ---------- | ----------------------------------- | ------ |
| superres    | 超分辨率模块                      |      |
| dnn_superres | 基于深度学习的超分放大            |      |


## 基础使用

```java
// 加载本地文件
String strImage = new File(context.getFilesDir(), "lfx.jpg").getAbsolutePath();
Mat mat = Imgcodecs.imread(strImage);

// 裁剪
Mat mat = lastMat.submat(t, b, l, r);

// 改变大小
Imgproc.resize(mat, mat, new org.opencv.core.Size(w, h));

// 调整格式
Mat rgbMat = new Mat();
Imgproc.cvtColor(mat, rgbMat, Imgproc.COLOR_GRAY2RGB);

// Mat -> byte
byte[] bytes = new byte[mat.width() * mat.height() * mat.channels()];
mat.get(0, 0, bytes);

// byte -> Mat
Mat mat = new Mat(h, w, CvType.CV_8UC3);
mat.put(0, 0, rgbBytes);

// YUV -> Mat：灰度图
static public Mat getImageGrayMat_YUV420(Image image) {
    if (image.getFormat() != ImageFormat.YUV_420_888)
        return null;
    Image.Plane[] planes = image.getPlanes();
    if (planes.length < 1) {
        Log.e(TAG, "getImageGrayBytes_YUV420: planes.length=" + planes.length);
        return null;
    }
    return new Mat(image.getHeight(), image.getWidth(), CvType.CV_8UC1, planes[0].getBuffer());
}
// YUV -> Mat: 彩图, Mat做中转
static public Mat getImageMat_YUV420(Image image) {
    if (image.getFormat() != ImageFormat.YUV_420_888)
        return null;
    Image.Plane[] planes = image.getPlanes();
    if (planes.length < 2) {
        Log.e(TAG, "getImageGrayBytes_YUV420: planes.length=" + planes.length);
        return null;
    }
    int cols = image.getWidth();
    int rows = image.getHeight();
    // YUV420_NV12格式
    Mat yuvMat = new Mat(rows * 3 / 2, cols, CvType.CV_8UC1);
    Mat yuvMatY = yuvMat.rowRange(0, rows);
    Mat yuvMatUV = yuvMat.rowRange(rows, rows * 3 / 2);
    // 摄像头数据提取
    Mat mY = new Mat(rows, cols, CvType.CV_8UC1, image.getPlanes()[0].getBuffer());
    Mat mUV = new Mat(rows / 2, cols, CvType.CV_8UC1, image.getPlanes()[1].getBuffer());
    mY.copyTo(yuvMatY);
    mUV.copyTo(yuvMatUV);
    return yuvMat;
}
// YUV -> Mat: 彩图, byte[]做中转
static public Mat getImageMat_YUV420(Image image) {
    if (image.getFormat() != ImageFormat.YUV_420_888)
        return null;
    Image.Plane[] planes = image.getPlanes();
    if (planes.length < 2) {
        Log.e(TAG, "getImageGrayBytes_YUV420: planes.length=" + planes.length);
        return null;
    }
    Image.Plane[] planes = image.getPlanes();
    ByteBuffer buffer1 = planes[0].getBuffer();
    ByteBuffer buffer2 = planes[1].getBuffer();

    byte[] bytes = new byte[(int)(image.getWidth() * image.getHeight() * 3 / 2)];
    buffer1.get(bytes, 0, buffer1.remaining());
    buffer2.get(bytes, image.getWidth() * image.getHeight(), buffer2.remaining());

    Mat yuvMat = new Mat(image.getHeight() * 3 / 2, image.getWidth(), CvType.CV_8UC1);
    yuvMat.put(0, 0, bytes);
    return yuvMat;
}
// 保存成文件
static public void saveMat(Context context, String fileName, Mat mat) {
    String strPath = context.getExternalFilesDir(Environment.DIRECTORY_PICTURES).getAbsolutePath();
    File file = new File(strPath, fileName);
    Log.e(TAG, "saveMat: " + file.getAbsolutePath());
    Imgcodecs.imwrite(file.getAbsolutePath(), mat);
}

// 旋转、镜像
byte[] resetImage(Mat mat, int orientation, boolean flip) {
    switch (orientation) {
        case 90:
            Core.rotate(mat, mat, Core.ROTATE_90_CLOCKWISE);
            break;
        case 180:
            Core.rotate(mat, mat, Core.ROTATE_180);
            break;
        case 270:
            Core.rotate(mat, mat, Core.ROTATE_90_COUNTERCLOCKWISE);
            break;
    }
    if(flip)
        Core.flip(mat, mat, 1); // 镜像
    byte[] imageBuf = new byte[mat.width() * mat.height()];
    mat.get(0, 0, imageBuf);
    return imageBuf;
}

// mat -> bitmap
private void show(Mat mat) {
    if (mShowView != null) {
        Bitmap bitmap;
        bitmap = Bitmap.createBitmap(mat.width(), mat.height(), Bitmap.Config.RGB_565);
        Utils.matToBitmap(mat, bitmap);
        new Handler(context.getMainLooper()).post(() -> mShowView.setImageBitmap(bitmap));
    }
}

// bitmap -> map
Mat mat = new Mat();
Utils.bitmapToMat(bitmap, mat);
if(mat.channels() == 4)
    Imgproc.cvtColor(mat, mat, Imgproc.COLOR_RGBA2RGB);
```

## 工程依赖

### Android.mk

```makefile

```
