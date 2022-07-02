---
title: CameraView
tags: 
    - CameraView
categories: 
    - Android
description: CameraView
date: 2022-06-29 16:08:16
updated: 2022-06-29 16:08:16
---

## CameraView

* [CameraView](https://www.jianshu.com/p/f63f296a920b)
+ [camera安卓开发文档](https://developer.android.google.cn/training/camera)
+ [官方源码](https://github.com/google/cameraview)
+ [camerakit-android](https://github.com/CameraKit/camerakit-android)
+ [otaliastudios](https://github.com/natario1/CameraView)

## 代码解析

### Demo
+ Camera 权限
    + `<uses-permission android:name="android.permission.CAMERA"/>`
    + 代码动态申请 `Manifest.permission.CAMERA`
+ activity_camera_view.xml -> CameraViewActivity 是简单测试用例
    + 创建 com.google.android.cameraview.CameraView 控件
    + 获取控件对象，直接调用`start`,`stop`即可

### CameraView
+ `createPreviewImpl`创建预览对象
    + SurfaceViewPreview(SurfaceView) / TextureViewPreview(TextureView)
        + SurfaceView = View + Surface + SurfaceHolder
        + `View` 控制生命周期，负责把Surface显示到屏幕
        + `Surface` 视图数据缓冲管理工具
        + `SurfaceHolder` 管理工具接口
            + 设置Surface参数：
                + 设置缓冲：`holder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS)`
    + 设置回调：监控 Surface 创建/销毁/变化
        + `surfaceCreated`: Surface 创建成功
        + `surfaceChanged`: Surface 配置成功 - 此函数回调之后此Surface才能用于创建会话
+ `Attributes`属性配置
    + `adjustViewBounds`保持相机纵横比
    + `facing`摄像头：前置/后置
    + `aspectRatio`相机预览纵横比：默认4:3
    + `autoFocus`连续自动对焦
    + `flash`闪光模式

### `start`启动
+ 这里仅分析`Camera2` + `SurfaceView`模型
+ `chooseCameraIdByFacing`: 选择摄像头
+ `collectCameraInfo`: 计算摄像头分辨率
    + 预览可用分辨率: SurfaceHolder
    + 拍照可用分辨率: JPEG
    + 检测配置的纵横比是否有效，无效则重置
+ `prepareImageReader`: 拍照相关预处理
    + 初始化拍照实例`ImageReader`
    + 设置回调`setOnImageAvailableListener`
    + 等待拍照指令即可触发
+ `startOpeningCamera`: 启动摄像头
    + `openCamera`: 监听`StateCallback`
        + `onOpened`, `onClosed`, `onDisconnected`, `onError`
    + `onOpened`
        + 得到`CameraDevice`对象
        + `startCaptureSession` 设置Camera会话
+ `startCaptureSession`
    + 最佳预览分辨率：`chooseOptimalSize`
        + 根据`View`大小适配等比例摄像头分辨率
        + 该操作在`SurfaceView`模型无意义，忽略即可
    + 设置预览模式
        + 创建摄像头预览请求Builder`mCamera.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW)`
        + Builder绑定预览视图`mPreviewRequestBuilder.addTarget(surface)`
    + 创建摄像头会话
        + `mCamera.createCaptureSession(Arrays.asList(surface, mImageReader.getSurface()), mSessionCallback, null);`
        + 包含两个surface：预览`mPreview.getSurface()` + 拍照`mImageReader.getSurface()`
        + 设置会话回调: `mSessionCallback`
        + 当创建新的Session时，旧有Session会被关掉，对应有onClosed回调
+ `mSessionCallback` 
    + 回调函数
        + `onConfigured`: 
            + Session创建好了，App可以通过它来向底层送CaptureRequest
            + 如果有CaptureRequest正在等待被处理，接下来onActive会被调用，否则onReady会被调用
        + `onConfigureFailed`: Session创建失败
        + `onSurfacePrepared`
            + 某一个Surface预分配Buffer完成后会调用该回调
            + 通过CameraCaptureSession.prepare(Surface)对buffer进行预分配
        + `onReady`: 当Session没有request处理时调用
        + `onActive`: 当Session开始处理request时调用
        + `onCaptureQueueEmpty`: 当Input Capture Request Queue空了后调用
        + `onClosed`: 该Session已经关闭
    + 获取会话对象`CameraCaptureSession`
    + 设置会话参数
        + 自动对焦：`updateAutoFocus`
        + 闪光模式: `updateFlash`
    + 发送循环预览请求
        + `mCaptureSession.setRepeatingRequest(mPreviewRequestBuilder.build(), mCaptureCallback, null);`

## CameraCaptureSession
+ capture/captureSingleRequest
    + 向Camera底层送一个CaptureRequest
    + 优先级比Repeating CaptureRequest要高
+ captureBurst/captureBurstRequests
    + 向Camera底层送一组CaptureRequests，优先级比Repeating CaptureRequest要高
    + 这一组CaptureRequest中间不能被其他CaptureRequest插入进来，这正是与连续调用Capture方法的区别
+ setRepeatingRequest/setSingleRepeatingRequest
    + 向Camera底层送一个CaptureRequest，底层会不停重复送这一个CaptureRequest
    + 不支持Reprocess CaptureRequest，因为Reprocess CaptureRequest是通过TotalCaptureResult创建而来的
+ setRepeatingBurst/setRepeatingBurstRequests
    + 向Camera底层送一组CaptureRequests，底层会不停重复送这一组CaptureRequests
    + 不支持Reprocess CaptureRequest
+ abortCaptures
    + 以最快的速度结束当前的Requests
    + in-flight captures可能成功也可能失败
    + Input Capture Request Queue会全部清空。
+ close
    + 关闭Session
    + 当切换到新的session时或关闭CameraDevice时，建议不要调用该方法
    + 直接调用createCaptureSession（未改变的Output Surfaces会被复用）或CameraDevice.close方法

+ getDevice()
    + 获取当前Session绑定的Camera Device。
+ prepare(Surface surface)
    + 预分配指定Surface的Buffer。会一次性申请该Surface允许的最大数量块Buffer。通常情况下，Surface里面的Buffer都是按需分配的，目的是为了减少启动时延和总体内存消耗。 通常情况下，我们可以在预览起来后，对拍照的Surface进行prepare，以优化第一次拍照性能，或者拍照过程中预览卡顿现象。
