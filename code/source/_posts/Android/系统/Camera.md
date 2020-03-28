---
title: Camera
tags: 
    - Camera
categories: 
    - Android
description: Camera
date: 2020-02-26 16:57:38
updated: 2020-03-28 19:30:25
---

## 第三方

+ [camera安卓开发文档](https://developer.android.google.cn/training/camera)

+ [camerakit-android](https://github.com/CameraKit/camerakit-android)
+ [boxing](https://github.com/bilibili/boxing)
+ [CameraView](https://github.com/natario1/CameraView)
+ [CameraView](https://github.com/CJT2325/CameraView)

+ [SampleCamera](https://github.com/qingmei2/SampleCamera)
  + 简单案例 - 学习使用
+ [cameraview](https://github.com/qingmei2/cameraview)
  + 自定义相机视图

## Camera

```java
/**
 * 根据视图宽高比，选择最佳相机像素比
 */
public final class CameraPreviewUtils {
    private static final String TAG = CameraPreviewUtils.class.getSimpleName();
    private static final int MIN_PREVIEW_PIXELS = 640 * 480;
    private static final int MAX_PREVIEW_PIXELS = 10000 * 1000; //1280 * 720;

    public static Point getBestPreview(Camera.Parameters parameters, Point screenResolution) {

        List<Camera.Size> rawSupportedSizes = parameters.getSupportedPreviewSizes();
        if (rawSupportedSizes == null) {
            Camera.Size defaultSize = parameters.getPreviewSize();
            return new Point(defaultSize.width, defaultSize.height);
        }

        List<Camera.Size> supportedPictureSizes = new ArrayList<Camera.Size>(rawSupportedSizes);
        Collections.sort(supportedPictureSizes, new Comparator<Camera.Size>() {
            @Override
            public int compare(Camera.Size a, Camera.Size b) {
                int aPixels = a.height * a.width;
                int bPixels = b.height * b.width;
                if (bPixels < aPixels) {
                    return -1;
                }
                if (bPixels > aPixels) {
                    return 1;
                }
                return 0;
            }
        });

        final double screenAspectRatio = (screenResolution.x > screenResolution.y) ?
                ((double) screenResolution.x / (double) screenResolution.y) :
                ((double) screenResolution.y / (double) screenResolution.x);

        Camera.Size selectedSize = null;
        double selectedMinus = -1;
        double selectedPreviewSize = 0;
        Iterator<Camera.Size> it = supportedPictureSizes.iterator();
        while (it.hasNext()) {
            Camera.Size supportedPreviewSize = it.next();
            int realWidth = supportedPreviewSize.width;
            int realHeight = supportedPreviewSize.height;
            if (realWidth * realHeight < MIN_PREVIEW_PIXELS) {
                it.remove();
                continue;
            } else if (realWidth * realHeight > MAX_PREVIEW_PIXELS) {
                it.remove();
                continue;
            } else {
                double aRatio = (supportedPreviewSize.width > supportedPreviewSize.height) ?
                        ((double) supportedPreviewSize.width / (double) supportedPreviewSize.height) :
                        ((double) supportedPreviewSize.height / (double) supportedPreviewSize.width);
                double minus = Math.abs(aRatio - screenAspectRatio);

                boolean selectedFlag = false;
                if ((selectedMinus == -1 && minus <= 0.25f)
                        || (selectedMinus >= minus && minus <= 0.25f)) {
                    selectedFlag = true;
                }
                if (selectedFlag) {
                    selectedMinus = minus;
                    selectedSize = supportedPreviewSize;
                    selectedPreviewSize = realWidth * realHeight;
                }
            }
        }

        if (selectedSize != null) {
            Camera.Size preview = selectedSize;
            return new Point(preview.width, preview.height);
        } else {
            Camera.Size defaultSize = parameters.getPreviewSize();
            return new Point(defaultSize.width, defaultSize.height);
        }
    }
}
```

```java
public class CameraFragment extends Fragment implements SurfaceHolder.Callback {
    private static final String TAG = CameraFragment.class.getSimpleName();
    // 设备
    private int mDisplayWidth;
    private int mDisplayHeight;
    // 视图
    private SurfaceView mSurfaceView;
    private SurfaceHolder mSurfaceHolder;
    protected boolean mIsCreateSurface = false;
    // 相机
    protected Camera mCamera;
    protected Camera.Parameters mCameraParam;
    protected boolean mFacingFront = true;
    protected int mCameraId = 0;

    public CameraFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_camera, container, false);
    }

    @Override
    public void onStart() {
        super.onStart();
        // 屏幕常亮
        getActivity().getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        // SurfaceView
        mSurfaceView = (SurfaceView) getActivity().findViewById(R.id.surfaceView);
        mSurfaceHolder = mSurfaceView.getHolder();
        mSurfaceHolder.addCallback(this);
        mSurfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
    }

    @Override
    public void onResume() {
        super.onResume();
        if (mIsCreateSurface)
            startPreview();
    }

    @Override
    public void onPause() {
        super.onPause();
        stopPreview();
    }

    @Override
    public void onStop() {
        super.onStop();
        stopPreview();
    }

    // ---------------------------------------------------------------------------------------------
    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        mIsCreateSurface = true;
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        mIsCreateSurface = false;
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
        if (holder.getSurface() == null) {
            return;
        }
        mDisplayWidth = width;
        mDisplayHeight = height;
        startPreview();
    }

    // ---------------------------------------------------------------------------------------------
    protected void startPreview() {
        if (mCamera == null) {
            mCamera = open();
            if(mCamera == null)
                return ;
            try {
                mCamera.setPreviewDisplay(mSurfaceHolder);
            } catch (IOException e) {
                e.printStackTrace();
                return ;
            }
        }
        if (mCameraParam == null)
            mCameraParam = mCamera.getParameters();

        mCameraParam.setPreviewFormat(ImageFormat.NV21);
        mCameraParam.setPictureFormat(ImageFormat.JPEG);
        mCameraParam.setJpegQuality(100);
        //设置自动对焦模式
        List<String> focusModes = mCameraParam.getSupportedFocusModes();
        for (String mode : focusModes) {
            if (mode.equals(Camera.Parameters.FOCUS_MODE_AUTO)) {
                mCameraParam.setFocusMode(Camera.Parameters.FOCUS_MODE_AUTO);
                break;
            }
        }
        // 矫正角度
        int degree = displayOrientation(getContext());
        mCamera.setDisplayOrientation(degree);
        // 设置后无效，camera.setDisplayOrientation方法有效
        mCameraParam.set("rotation", degree);
//        mPreviewDegree = mFacingFront ? degree : ((360 - degree) % 360);
        // 相机设定最佳像素
        Point point = CameraPreviewUtils.getBestPreview(mCameraParam,
                new Point(mDisplayWidth, mDisplayHeight));
        int previewWidth = point.x;
        int previewHight = point.y;
        mCameraParam.setPreviewSize(previewWidth, previewHight);
        mCameraParam.setPictureSize(previewWidth, previewHight);
        // 按比率充值视图
        int w = mDisplayWidth;
        int h = mDisplayHeight;
        if(mDisplayWidth < mDisplayHeight) {
            previewWidth = previewWidth ^ previewHight;
            previewHight = previewWidth ^ previewHight;
            previewWidth = previewWidth ^ previewHight;
        }
        if(w > (h * previewWidth / previewHight))
            h = w * previewHight / previewWidth;
        else
            w = h * previewWidth / previewHight;

            FrameLayout.LayoutParams cameraFL = new FrameLayout.LayoutParams(
                    (int) (w), (int) (h),
                    Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL);
            mSurfaceView.setLayoutParams(cameraFL);

        mCamera.setParameters(mCameraParam);

        try {
            mCamera.stopPreview();
//            mCamera.setErrorCallback(this);
//            mCamera.setPreviewCallback(this);
            mCamera.startPreview();
        } catch (RuntimeException e) {
            e.printStackTrace();
            releaseCamera(mCamera);
            mCamera = null;
        } catch (Exception e) {
            e.printStackTrace();
            releaseCamera(mCamera);
            mCamera = null;
        }
    }

    private Camera open() {
        Camera camera;
        int numCameras = Camera.getNumberOfCameras();
        if (numCameras == 0) {
            return null;
        }

        int index = 0;
        while (index < numCameras) {
            Camera.CameraInfo cameraInfo = new Camera.CameraInfo();
            Camera.getCameraInfo(index, cameraInfo);
            if (cameraInfo.facing == (mFacingFront ? Camera.CameraInfo.CAMERA_FACING_FRONT : Camera.CameraInfo.CAMERA_FACING_BACK)) {
                break;
            }
            index++;
        }

        if (index < numCameras) {
            mCameraId = index;
            camera = Camera.open(index);
        } else {
            mCameraId = 0;
            camera = Camera.open(0);
        }
        return camera;
    }
    // 相机角度矫正
    private int displayOrientation(Context context) {
        WindowManager windowManager = (WindowManager) context.getSystemService(Context.WINDOW_SERVICE);
        int rotation = windowManager.getDefaultDisplay().getRotation();
        int degrees = 0;
        switch (rotation) {
            case Surface.ROTATION_0:
                degrees = 0;
                break;
            case Surface.ROTATION_90:
                degrees = 90;
                break;
            case Surface.ROTATION_180:
                degrees = 180;
                break;
            case Surface.ROTATION_270:
                degrees = 270;
                break;
            default:
                degrees = 0;
                break;
        }
        int result = 0;
        Camera.CameraInfo info = new Camera.CameraInfo();
        Camera.getCameraInfo(mCameraId, info);
        if (info.facing == Camera.CameraInfo.CAMERA_FACING_FRONT) {
            result = (info.orientation + degrees) % 360;
            result = (360 - result) % 360;
        } else {
            result = (info.orientation - degrees + 360) % 360;
        }
        return result;
    }

    protected void stopPreview() {
        if (mCamera != null) {
            try {
                mCamera.setErrorCallback(null);
                mCamera.setPreviewCallback(null);
                mCamera.stopPreview();
            } catch (RuntimeException e) {
                e.printStackTrace();
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                releaseCamera(mCamera);
                mCamera = null;
                mCameraParam = null;
            }
        }
        if (mSurfaceHolder != null) {
            mSurfaceHolder.removeCallback(this);
        }
    }

    public static void releaseCamera(Camera camera) {
        try {
            camera.release();
        } catch (RuntimeException e2) {
            e2.printStackTrace();
        } catch (Exception e1) {
            e1.printStackTrace();
        } finally {
        }
    }
}
```