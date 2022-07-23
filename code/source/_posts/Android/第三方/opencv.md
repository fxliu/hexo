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

## 基础使用

```java
// 加载本地文件
String strImage = new File(context.getFilesDir(), "lfx.jpg").getAbsolutePath();
Mat mat = Imgcodecs.imread(strImage);

// 改变大小
Imgproc.resize(mat, mat, new org.opencv.core.Size(w, h));

// 调整格式
Mat rgbMat = new Mat();
Imgproc.cvtColor(mat, rgbMat, Imgproc.COLOR_GRAY2RGB);

// Mat -> byte
byte[] bytes = new byte[mat.width() * mat.height() * mat.channels()];
mat.get(0, 0, bytes);

// YUV -> Mat
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
```
