---
title: SurfaceView
tags: 
    - SurfaceView
categories: 
    - Android
description: SurfaceView
date: 2022-07-26 09:59:13
updated: 2022-07-26 09:59:13
---

## 基础

### SurfaceHolder.Callback

```java
// 方向感应
DisplayOrientationDetector mDisplayOrientationDetector;
mDisplayOrientationDetector = new DisplayOrientationDetector(mSurfaceView.getContext()) {
    @Override
    public void onDisplayOrientationChanged(int displayOrientation) {
        mDisplayOrientation = displayOrientation;
    }
};
// SurfaceHolder.Callback
SurfaceHolder holder = mSurfaceView.getHolder();
holder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
holder.addCallback(new SurfaceHolder.Callback() {
    @Override
    public void surfaceCreated(SurfaceHolder h) {
        mDisplayOrientationDetector.enable(mSurfaceView.getDisplay());
    }

    @Override
    public void surfaceChanged(SurfaceHolder h, int format, int width, int height) {
        if (!ViewCompat.isInLayout(mSurfaceView)) {
            mFormat = format;
            // ...
        }
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder h) {
        mDisplayOrientationDetector.disable();
    }
});

// holder.setType
SURFACE_TYPE_NORMAL: 用RAM缓存原生数据的普通Surface
SURFACE_TYPE_HARDWARE: 适用于DMA(Direct memory access )引擎和硬件加速的Surface
SURFACE_TYPE_GPU: 适用于GPU加速的Surface
SURFACE_TYPE_PUSH_BUFFERS: 表明该Surface不包含原生数据，Surface用到的数据由其他对象提供，在Camera图像预览中就使用该类型的Surface，有Camera负责提供给预览Surface数据，这样图像预览会比较流畅。如果设置这种类型则就不能调用lockCanvas来获取Canvas对象了。
```

## 自绘

```java
// 自绘
SurfaceHolder holder = mSurfaceView.getHolder();
Canvas canvas = holder.lockCanvas();
// Canvas canvas = mSurface.lockHardwareCanvas();   // GPU硬加速 Canvas
canvas.drawBitmap(bitmap, 0, 0, new Paint());
holder.unlockCanvasAndPost(canvas);
```
