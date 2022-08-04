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

## Camera2

```java
// 权限
static final private String[] mCameraPermissions = new String[]{
        Manifest.permission.CAMERA
};
// CameraManager
private final CameraManager mCameraManager;
mCameraManager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);
// 摄像头
CameraDevice mCamera;
CameraCharacteristics mCharacteristics;
// 会话
CameraCaptureSession mCaptureSession;
// openCamera
mCharacteristics = mCameraManager.getCameraCharacteristics(cameraId);
mCameraManager.openCamera(cameraId, mCameraStateCallback, null);
CameraDevice.StateCallback mCameraStateCallback = new CameraDevice.StateCallback() {
    @Override
    public void onOpened(@NonNull CameraDevice camera) {
        Log.d(TAG, "CameraDevice.StateCallback: onOpened");
        mCamera = camera;
    }

    @Override
    public void onDisconnected(@NonNull CameraDevice camera) {
        Log.e(TAG, "CameraDevice.StateCallback: onDisconnected");
        stop();
    }

    @Override
    public void onError(@NonNull CameraDevice camera, int error) {
        Log.e(TAG, "CameraDevice.StateCallback: onError, id=" + camera.getId() + ", err=" + error);
        stop();
    }
};
// createCaptureSession: 传入多个 Surface
public void startCaptureSession(List<EsSurfaceImpl> readers) {
    try {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.P) {
            List<OutputConfiguration> configurations = new Vector<>();
            for (EsSurfaceImpl reader : readers)
                configurations.add(new OutputConfiguration(reader.getSurface()));
            SessionConfiguration sessionConfiguration = new SessionConfiguration(
                    SessionConfiguration.SESSION_REGULAR,
                    configurations,
                    Runnable::run,
                    mSessionCallback
            );
            mCamera.createCaptureSession(sessionConfiguration);
        } else {
            List<Surface> surfaces = new Vector<>();
            for (EsSurfaceImpl reader : readers)
                surfaces.add(reader.getSurface());
            mCamera.createCaptureSession(surfaces, mSessionCallback, null);
        }
    } catch (CameraAccessException e) {
        e.printStackTrace();
    }
}
CameraCaptureSession.StateCallback mSessionCallback = new CameraCaptureSession.StateCallback() {
    @Override
    public void onConfigured(@NonNull CameraCaptureSession cameraCaptureSession) {
        Log.d(TAG, "StateCallback.onConfigured");
        mCaptureSession = cameraCaptureSession;
    }

    @Override
    public void onConfigureFailed(@NonNull CameraCaptureSession cameraCaptureSession) {
        Log.e(TAG, "Failed to configure capture session.");
    }
};
// createCaptureRequest
public CaptureRequest.Builder createCaptureRequest(List<EsSurfaceImpl> readers, int templateType) {
    try {
        CaptureRequest.Builder builder = mCamera.createCaptureRequest(templateType);
        // builder.set(CaptureRequest.JPEG_ORIENTATION, mCharacteristics.get(CameraCharacteristics.SENSOR_ORIENTATION));
        for (EsSurfaceImpl reader : readers)
            builder.addTarget(reader.getSurface());
        return builder;
    } catch (CameraAccessException e) {
        e.printStackTrace();
    }
    return null;
}
// setRepeatingRequest
public void sendRequest(CaptureRequest request, boolean bRepeating, CameraCaptureSession.CaptureCallback listener) {
    try {
        if (bRepeating)
            mCaptureSession.setRepeatingRequest(request, listener, null);
        else
            mCaptureSession.capture(request, listener, null);
    } catch (CameraAccessException e) {
        e.printStackTrace();
    }
}
```
