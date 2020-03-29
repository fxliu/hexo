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

+ [cameraview](https://github.com/qingmei2/cameraview)
  + Camera 1 API on API Level 9-20 and Camera2 on 21 and above

+ [camerakit-android](https://github.com/CameraKit/camerakit-android)
+ [boxing](https://github.com/bilibili/boxing)
+ [CameraView](https://github.com/natario1/CameraView)
+ [CameraView](https://github.com/CJT2325/CameraView)


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
public class CameraUtil {
    private static final String TAG = CameraUtil.class.getSimpleName();
    // 摄像头参数
    private Camera mCamera;
    private Camera.Parameters mCameraParameters;
    private final Camera.CameraInfo mCameraInfo = new Camera.CameraInfo();
    // 摄像头选择
    private static final int INVALID_CAMERA_ID = -1;
    private int mFacing;
    private int mCameraId;

    // ---------------------------------------------------------------------------------------------
    // 监控设备角度
    OrientationEventListener mOrientationEventListener;
    public void regeditOrientationListener(Context context, View view) {
        mOrientationEventListener = new OrientationEventListener(context) {
            /** This is either Surface.Rotation_0, _90, _180, _270, or -1 (invalid). */
            @Override
            public void onOrientationChanged(int orientation) {
                if (orientation == OrientationEventListener.ORIENTATION_UNKNOWN) {
                    return;
                }
                final int rotation = ViewCompat.getDisplay(view).getRotation();
                setDisplayOrientation(rotation);
            }
        };
        mOrientationEventListener.enable();
    }
    public void unregeditOrientationListener(){
        mOrientationEventListener.disable();
        mOrientationEventListener = null;
    }
    // ---------------------------------------------------------------------------------------------
    // 打开摄像头
    public Camera open(int facing) {
        Log.e(TAG, "open");
        if (mCamera != null) {
            release();
        }
        // 选择摄像头
        mFacing = facing;
        chooseCamera();
        // 打开摄像头
        mCamera = Camera.open(mCameraId);
        // Supported preview sizes
        // mCameraParameters.getSupportedPreviewSizes();
        // mCameraParameters.getSupportedPictureSizes();
        // 配置参数
        mCameraParameters = mCamera.getParameters();
        return mCamera;
    }
    // 关闭摄像头
    public void release() {
        try {
            if(null != mCamera) {
                mCamera.release();
                mCamera = null;
            }
            if(null != mCameraParameters)
                mCameraParameters = null;
        } catch (Exception e2) {
            e2.printStackTrace();
        }
    }
    public void start(SurfaceHolder holder, Camera.PreviewCallback pcb) {
        if(null == mCamera) return ;
        try {
            mCameraParameters.setPreviewFormat(ImageFormat.NV21);
            mCameraParameters.setPictureFormat(ImageFormat.JPEG);
            mCameraParameters.setJpegQuality(100);
            // 特殊参数
            setAutoFocusInternal(true);
            // setFlashInternal(mFlash);
            setDisplayOrientation(mDisplayOrientation);

            mCamera.setParameters(mCameraParameters);
            mCamera.setPreviewDisplay(holder);
        } catch (IOException e) {
            e.printStackTrace();
            return ;
        }
        try {
            mCamera.stopPreview();
//            mCamera.setErrorCallback(this);
            mCamera.setPreviewCallback(pcb);
            mCamera.startPreview();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public void stop() {
        if(null == mCamera)
            return ;
        mCamera.setPreviewCallback(null);
        mCamera.stopPreview();
    }
    public Camera.Parameters getCameraParameters() {
        return mCameraParameters;
    }
    // ---------------------------------------------------------------------------------------------
    // 选择摄像头
    private void chooseCamera() {
        for (int index = 0, count = Camera.getNumberOfCameras(); index < count; index++) {
            Camera.getCameraInfo(index, mCameraInfo);
            if (mCameraInfo.facing == mFacing) {
                mCameraId = index;
                return;
            }
        }
        mCameraId = INVALID_CAMERA_ID;
    }
    // ---------------------------------------------------------------------------------------------
    // 大小
    public void setSize(int w, int h) {
        if(0 != w && 0 != h) {
            mCameraParameters.setPreviewSize(w, h);
            mCameraParameters.setPictureSize(w, h);
        }
    }
    // 计算方向
    int mDisplayOrientation = 0;
    public void setDisplayOrientation(int displayOrientation) {
        mDisplayOrientation = displayOrientation;
        if (null != mCamera) {
            mCameraParameters.setRotation(displayOrientation(displayOrientation));
            mCamera.setDisplayOrientation(displayOrientation(displayOrientation));
        }
    }

    // 相机角度矫正
    private int displayOrientation(int rotation) {
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
    // ---------------------------------------------------------------------------------------------
    // 自动对焦
    private boolean setAutoFocusInternal(boolean autoFocus) {
        if (null != mCamera) {
            final List<String> modes = mCameraParameters.getSupportedFocusModes();
            if (autoFocus && modes.contains(Camera.Parameters.FOCUS_MODE_CONTINUOUS_PICTURE)) {
                mCameraParameters.setFocusMode(Camera.Parameters.FOCUS_MODE_CONTINUOUS_PICTURE);
            } else if (modes.contains(Camera.Parameters.FOCUS_MODE_FIXED)) {
                mCameraParameters.setFocusMode(Camera.Parameters.FOCUS_MODE_FIXED);
            } else if (modes.contains(Camera.Parameters.FOCUS_MODE_INFINITY)) {
                mCameraParameters.setFocusMode(Camera.Parameters.FOCUS_MODE_INFINITY);
            } else {
                mCameraParameters.setFocusMode(modes.get(0));
            }
            return true;
        } else {
            return false;
        }
    }
    // ---------------------------------------------------------------------------------------------
    // 闪光灯控制
    private static final SparseArrayCompat<String> FLASH_MODES = new SparseArrayCompat<>();
    static {
        FLASH_MODES.put(0, Camera.Parameters.FLASH_MODE_OFF);
        FLASH_MODES.put(1, Camera.Parameters.FLASH_MODE_ON);
        FLASH_MODES.put(2, Camera.Parameters.FLASH_MODE_TORCH);
        FLASH_MODES.put(3, Camera.Parameters.FLASH_MODE_AUTO);
        FLASH_MODES.put(4, Camera.Parameters.FLASH_MODE_RED_EYE);
    }
    private boolean setFlashInternal(int flash) {
        if (null == mCamera)
            return false;
        List<String> modes = mCameraParameters.getSupportedFlashModes();
        String mode = FLASH_MODES.get(flash);
        if (modes != null && modes.contains(mode)) {
            mCameraParameters.setFlashMode(mode);
            return true;
        }
        String currentMode = FLASH_MODES.get(flash);
        if (modes == null || !modes.contains(currentMode)) {
            mCameraParameters.setFlashMode(Camera.Parameters.FLASH_MODE_OFF);
            return true;
        }
        return false;
    }
}
```

```java
public class CameraFragment extends Fragment implements SurfaceHolder.Callback, Camera.PreviewCallback {
    private static final String TAG = CameraFragment.class.getSimpleName();
    // 设备
    private int mDisplayWidth;
    private int mDisplayHeight;
    // 视图
    private SurfaceView mSurfaceView;
    private SurfaceHolder mSurfaceHolder;
    protected boolean mIsCreateSurface = false;
    // 相机
    protected boolean mFacingFront = true;
    protected CameraUtil mCameraUtil;

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
        mCameraUtil = new CameraUtil();
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
        mIsCreateSurface = true;
        mDisplayWidth = width;
        mDisplayHeight = height;
        startPreview();
    }

    @Override
    public void onPreviewFrame(byte[] data, Camera camera) {
    }

    // ---------------------------------------------------------------------------------------------
    protected void startPreview() {
        mCameraUtil.open(mFacingFront ? 1 : 0);
        // 相机设定最佳像素
        Point point = CameraPreviewUtils.getBestPreview(mCameraUtil.getCameraParameters(),
                new Point(mDisplayWidth, mDisplayHeight));
        int previewWidth = point.x;
        int previewHight = point.y;
        mCameraUtil.setSize(previewWidth, previewHight);
        // 设置视图显示区域：按相机比率等比拉伸
        int w = mDisplayWidth;
        int h = mDisplayHeight;
        if (mDisplayWidth < mDisplayHeight) {
            previewWidth = previewWidth ^ previewHight;
            previewHight = previewWidth ^ previewHight;
            previewWidth = previewWidth ^ previewHight;
        }
        if (w > (h * previewWidth / previewHight))
            h = w * previewHight / previewWidth;
        else
            w = h * previewWidth / previewHight;

        FrameLayout.LayoutParams cameraFL = new FrameLayout.LayoutParams(
                (int) (w), (int) (h),
                Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL);
        mSurfaceView.setLayoutParams(cameraFL);

        try {
            mCameraUtil.setDisplayOrientation(ViewCompat.getDisplay(Objects.requireNonNull(this.getView())).getRotation());
            mCameraUtil.start(mSurfaceHolder, this);
//            mCamera.setErrorCallback(this);
        } catch (RuntimeException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    protected void stopPreview() {
        mCameraUtil.stop();
        mCameraUtil.release();
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