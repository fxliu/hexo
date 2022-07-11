---
title: Camera2
tags: 
    - Camera2
categories: 
    - Android
description: Camera2
date: 2022-06-30 18:58:52
updated: 2022-06-30 18:58:52
---

## 资料
+ [cameraview](https://github.com/google/cameraview)
+ [AndroidCamera2API详解](https://blog.csdn.net/qq_42194101/category_11338722.html)
+ [极客笔记-AndroidCamera2API](https://deepinout.com/android-camera-official-documentation)

### 工程

+ [lib_escamera](\svn\esface\trunk\Android\SeetaFace6Demo\lib_escamera)
  + SurfaceView + Camera2

## 流程

+ 打开摄像头：`CameraManager`
  + `mCameraManager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);`
  + 摄像头ID: `mCameraManager.getCameraIdList()`
  + 摄像头参数: `mCharacteristics = mCameraManager.getCameraCharacteristics(cameraId)`
    + 方向：`characteristics.get(CameraCharacteristics.LENS_FACING) == CameraCharacteristics.LENS_FACING_FRONT`
    + 分辨率：`mCharacteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);`
  + openCamera: ` mCameraManager.openCamera(cameraId, mCameraStateCallback, handler)`
    + 回调：mCameraStateCallback
    + onOpened：得到摄像头对象 CameraDevice
+ 创建接收Surface: ImageReader/SurfaceView
  + SurfaceView: `mSurfaceView = view.findViewById(R.id.surface_view);`
    + 设置`SurfaceHolder.Callback`
    + 会话绑定Surface之前，需确保surface已创建，且大小有效；即回调`surfaceChanged`之后
    + View自动接收会话请求结果并显示
  + ImageReader: `mImageReader = ImageReader.newInstance(640, 480, ImageFormat.JPEG, 2);`
    + 根据摄像头支持分辨率创建 ImageReader
    + 设置回调监听会话请求结果
      + `mImageReader.setOnImageAvailableListener(mOnImageAvailableListener, null)`
  + surface
    + 预览组件：SurfaceView、GLSurfaceView、TextureView
    + 拍照组件：ImageReader
    + 录像组件：MediaRecorder、MediaCodec
+ 创建会话
  + android.os.Build.VERSION_CODES.P
    + 基于Surface生成OutputConfiguration：`new OutputConfiguration(mImageReader.getSurface())`
      + 主要是采集Surface大小，图片格式等参数，用于自动适配合适的摄像头属性
    + OutputConfiguration 列表：`Collections.singletonList(new OutputConfiguration(mImageReader.getSurface()))`
    + 创建SessionConfiguration: 
      + `new SessionConfiguration(SessionConfiguration.SESSION_REGULAR, outputConfigurationList, null, mSessionCallback)`
    + 创建CaptureSession: `mCamera.createCaptureSession(sessionConfiguration)`
  + 创建CaptureSession - 低版本兼容
    + `mCamera.createCaptureSession(Collections.singletonList(mImageReader.getSurface()), mSessionCallback, null)`
    + mSessionCallback -> onConfigured: 获得 CameraCaptureSession 对象
+ 请求图像 - 基于CameraCaptureSession
  + 创建请求：根据业务需要选择模板
    + `mCaptureRequest = mCamera.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW)`
    + 绑定到surface: `mCaptureRequest.addTarget(mImageReader.getSurface())`
  + 发送请求 - 循环发送
    + `mCaptureSession.setRepeatingRequest(mCaptureRequest.build(), mCaptureCallback, null);`

## openCamera

+ 第二次打开，会自动关闭第一次句柄，触发StateCallback.onDisconnected
+ 回调
  + onClosed: 底层真正关闭CameraDevice后回调
  + onDisconnected: 
    + openCamera失败触发
    + 摄像头被拔出
    + 高优先级APP抢占
    + 收到该回调，需要执行`CameraDevice.close`
  + onError: 底层出现错误，无法正常出图
    + 收到该回调，需要执行`CameraDevice.close`
  + onOpened: 打开成功

```java
CameraManager mCameraManager;
mCameraManager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);
// 摄像头数量
final String[] ids = mCameraManager.getCameraIdList();

// 摄像头能力检查: CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL_FULL
CameraCharacteristics characteristics = mCameraManager.getCameraCharacteristics(id);
Integer level = characteristics.get(CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL);

// 摄像头位置检查: CameraController.Facing.FACING_FRONT / FACING_BACK / FACING_EXTERNAL
Integer internal = characteristics.get(CameraCharacteristics.LENS_FACING);

// Camera设备支持的功能列表
int [] capabilities = characteristics.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES);
```

## StreamConfigurationMap

```java
// 摄像头输出流配置信息：比如支持图像格式，支持分辨率等
mCameraCharacteristics = mCameraManager.getCameraCharacteristics(mCameraId);
StreamConfigurationMap map = mCameraCharacteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
// 返回指定格式支持的输出流Size列表
map.getOutputSizes(ImageFormat.JPEG);
map.getOutputSizes(SurfaceHolder.class);
map.getOutputSizes(SurfaceTexture.class);
```

+ `isOutputSupportedFor`
  + 是否支持指定 class/surface/format
+ `getOutputSizes`
  + 获取支持指定 class/format 的输出流size
+ `getOutputMinFrameDuration` / `getOutputStallDuration`
  + 指定 class/format 的最小/高帧率
+ `getHighSpeedVideoSizes`
  + 高帧率流
+ `getHighResolutionOutputSizes`
  + 高分辨率流
+ format
  + ImageFormat.JPEG / ImageFormat.RAW12 / ImageFormat.YUV_420_888 / PixelFormat.RGB_888
+ class
  + `SurfaceHolder.class` / `SurfaceTexture.class`

## 显示控制

```java
// 摄像头方向 - int 0/90/180/270
characteristics.get(CameraCharacteristics.SENSOR_ORIENTATION);
// UI显示方向 - Surface.ROTATION_0/90/180/270
mSurfaceView.getDisplay().getRotation();
// 视频大小 - 摄像头根据该参数适配分辨率
// 这里的[w,h]根据摄像头分辨率设置
mSurfaceView.getHolder().setFixedSize(w, h);
// UI 区域大小 - 视频拉伸显示到UI区域
// 这里的[w,h]根据UI设置, 需要考虑偏转
ViewGroup.LayoutParams layoutParams = mSurfaceView.getLayoutParams();
layoutParams.width = w;
layoutParams.height = h;
mSurfaceView.setLayoutParams(layoutParams);
```

## 会话
### 会话请求回调(CaptureCallback)
  + mCaptureSession.setRepeatingRequest(mPreviewRequestBuilder.build(), mCaptureCallback, null);
  + 请求开始：`onCaptureStarted`
  + 部分完成：`onCaptureProgressed`
  + 请求完成：`onCaptureCompleted`
  + 丢帧：`onCaptureBufferLost`
  + 请求失败：`onCaptureFailed`
  + 请求终止：`onCaptureSequenceAborted`
      + 通常由`stopRepeating` `abortCaptures`触发
  + 请求序列完成: `onCaptureSequenceCompleted`
