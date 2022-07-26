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
```

## 自绘

```java
// 自绘
SurfaceHolder holder = mSurfaceView.getHolder();
Canvas canvas = holder.lockCanvas();
canvas.drawBitmap(bitmap, 0, 0, new Paint());
holder.unlockCanvasAndPost(canvas);
```
