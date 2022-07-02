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
+ [AndroidCamera2API详解](https://blog.csdn.net/qq_42194101/category_11338722.html)
+ [极客笔记-AndroidCamera2API](https://deepinout.com/android-camera-official-documentation)

## 流程

+ `Context.getSystemService(Context.CAMERA_SERVICE);`
+ `CameraManager`
  + getCameraIdList
  + getCameraCharacteristics
  + openCamera
+ `openCamera` -> `CameraDevice`
  + close
  + createCaptureSession
    + 绑定到多个 surface
    + surface
      + 预览组件：SurfaceView、GLSurfaceView、TextureView
      + 拍照组件：ImageReader
      + 录像组件：MediaRecorder、MediaCodec
  + createCaptureRequest -> CaptureRequest.Builder
    + mCamera.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW): 指定请求
    + addTarget：绑定surface
+ `createCaptureSession` -> `CameraCaptureSession`
  + 发送/终止请求
    + capture/captureBurst
    + setRepeatingRequest/setRepeatingBurst
    + stopRepeating/abortCaptures
  + 从Camera设备获取数据流
  + 图像数据在处理(Reprocess)
    + isReprocessable
    + getInputSurface
  + 切换到离线会话
  + 性能优化
    + 延迟Surface
    + 预分配Buffer
  + 动态更新Out Configuration
+ 2层请求列表
  + RepeatingRequest List: 低优先
  + PendingRequest Queue
+ 请求 -> surface
  + Request -> Image Buffer -> surface

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
+ isOutputSupportedFor
  + 是否支持指定 class/surface/format
+ getOutputSizes
  + 支持指定 class/format 的输出流size
+ getOutputMinFrameDuration/getOutputStallDuration
  + 指定 class/format 的最小/高帧率
+ getHighSpeedVideoSizes
  + 高帧率流
+ getHighResolutionOutputSizes
  + 高分辨率流
+ fmt
  + ImageFormat.JPEG / ImageFormat.RAW12 / ImageFormat.YUV_420_888 / PixelFormat.RGB_888
+ 实际应用注意输出流Size，要支持后续所有surface需求：预览 / 拍照 / 录像
```java
// 摄像头输出流配置信息：比如支持图像格式，支持分辨率等
mCameraCharacteristics = mCameraManager.getCameraCharacteristics(mCameraId);
StreamConfigurationMap map = mCameraCharacteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
// 返回指定Class支持的输出流Size列表
map.getOutputSizes(mPreview.getOutputClass());
// 返回指定格式支持的输出流Size列表
map.getOutputSizes(ImageFormat.JPEG);
```
