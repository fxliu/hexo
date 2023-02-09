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

## 资料

* [Android官方示例](https://github.com/android/camera-samples)
* [demo](\svn\cloud_visitor\trunk\4_android\guard\)
  * \com\es\util\CameraUtils


### other

+ [boxing](https://github.com/bilibili/boxing)
    + 基于MVP模式的Android多媒体选择器
    + 支持多/单图片选择和预览，单图裁剪功能
    + 支持gif
    + 支持视频选择功能
    + 提供图片压缩
    + 多图生成gif（checkout feature/gif-encode), 见 Bilibili/BurstLinker
+ libyuv

## 性能提升

+ camera.addCallbackBuffer
    + 需要利用 onPreviewFrame 采集数据时, 可以提前设定图片缓冲区, 并持续复用

## Camera Demo

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

```java

/* 示例 - 虹软人脸识别Demo
 cameraHelper = new CameraHelper.Builder()
 .previewViewSize(new Point(640, 480))    // new Point(previewView.getMeasuredWidth(), previewView.getMeasuredHeight())
 .rotation(180)
 .specificCameraId(0)
 .isMirror(false)
 .previewOn(previewView)                  // 兼容 TextureView / SurfaceView
 // .cameraListener(cameraListener)
 .build();
 */

public class CameraHelper implements Camera.PreviewCallback {
    private static final String TAG = "CameraHelper";
    private Camera mCamera;
    private int mCameraId;
    private Point previewViewSize;
    private View previewDisplayView;
    private Camera.Size previewSize;
    private Point specificPreviewSize;
    private int displayOrientation = 0;
    private int rotation;
    private int additionalRotation;
    private boolean isMirror = false;

    private Integer specificCameraId = null;
    private CameraListener cameraListener;

    private CameraHelper(Builder builder) {
        previewDisplayView = builder.previewDisplayView;
        specificCameraId = builder.specificCameraId;
        cameraListener = builder.cameraListener;
        rotation = builder.rotation;
        additionalRotation = builder.additionalRotation;
        previewViewSize = builder.previewViewSize;
        specificPreviewSize = builder.previewSize;
        if (builder.previewDisplayView instanceof TextureView) {
            isMirror = builder.isMirror;
        } else if (isMirror) {
            throw new RuntimeException("mirror is effective only when the preview is on a textureView");
        }
    }

    public void init() {
        if (previewDisplayView instanceof TextureView) {
            ((TextureView) this.previewDisplayView).setSurfaceTextureListener(textureListener);
        } else if (previewDisplayView instanceof SurfaceView) {
            ((SurfaceView) previewDisplayView).getHolder().addCallback(surfaceCallback);
        }

        if (isMirror) {
            previewDisplayView.setScaleX(-1);
        }
    }

    public void start() {
        synchronized (this) {
            if (mCamera != null) {
                return;
            }
            //相机数量为2则打开1,1则打开0,相机ID 1为前置，0为后置
            mCameraId = Camera.getNumberOfCameras() - 1;
            //若指定了相机ID且该相机存在，则打开指定的相机
            if (specificCameraId != null && specificCameraId <= mCameraId) {
                mCameraId = specificCameraId;
            }

            //没有相机
            if (mCameraId == -1) {
                if (cameraListener != null) {
                    cameraListener.onCameraError(new Exception("camera not found"));
                }
                return;
            }
            if (mCamera == null) {
                mCamera = Camera.open(mCameraId);
            }

            displayOrientation = getCameraOri(rotation);
            mCamera.setDisplayOrientation(displayOrientation);
            try {
                Camera.Parameters parameters = mCamera.getParameters();
                parameters.setPreviewFormat(ImageFormat.NV21);

                //预览大小设置
                previewSize = parameters.getPreviewSize();
                List<Camera.Size> supportedPreviewSizes = parameters.getSupportedPreviewSizes();
                if (supportedPreviewSizes != null && supportedPreviewSizes.size() > 0) {
                    previewSize = getBestSupportedSize(supportedPreviewSizes, previewViewSize);
                }
                parameters.setPreviewSize(previewSize.width, previewSize.height);

                //对焦模式设置
                List<String> supportedFocusModes = parameters.getSupportedFocusModes();
                if (supportedFocusModes != null && supportedFocusModes.size() > 0) {
                    if (supportedFocusModes.contains(Camera.Parameters.FOCUS_MODE_CONTINUOUS_PICTURE)) {
                        parameters.setFocusMode(Camera.Parameters.FOCUS_MODE_CONTINUOUS_PICTURE);
                    } else if (supportedFocusModes.contains(Camera.Parameters.FOCUS_MODE_CONTINUOUS_VIDEO)) {
                        parameters.setFocusMode(Camera.Parameters.FOCUS_MODE_CONTINUOUS_VIDEO);
                    } else if (supportedFocusModes.contains(Camera.Parameters.FOCUS_MODE_AUTO)) {
                        parameters.setFocusMode(Camera.Parameters.FOCUS_MODE_AUTO);
                    }
                }
                mCamera.setParameters(parameters);
                if (previewDisplayView instanceof TextureView) {
                    mCamera.setPreviewTexture(((TextureView) previewDisplayView).getSurfaceTexture());
                } else {
                    mCamera.setPreviewDisplay(((SurfaceView) previewDisplayView).getHolder());
                }
                mCamera.setPreviewCallback(this);
                mCamera.startPreview();
                if (cameraListener != null) {
                    cameraListener.onCameraOpened(mCamera, mCameraId, displayOrientation, isMirror);
                }
            } catch (Exception e) {
                if (cameraListener != null) {
                    cameraListener.onCameraError(e);
                }
            }
        }
    }

    private int getCameraOri(int rotation) {
        int degrees = rotation * 90;
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
                break;
        }
        additionalRotation /= 90;
        additionalRotation *= 90;
        degrees += additionalRotation;
        int result;
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

    public void stop() {
        synchronized (this) {
            if (mCamera == null) {
                return;
            }
            mCamera.setPreviewCallback(null);
            mCamera.stopPreview();
            mCamera.release();
            mCamera = null;
            if (cameraListener != null) {
                cameraListener.onCameraClosed();
            }
        }
    }

    public boolean isStopped() {
        synchronized (this) {
            return mCamera == null;
        }
    }

    public void release() {
        synchronized (this) {
            stop();
            previewDisplayView = null;
            specificCameraId = null;
            cameraListener = null;
            previewViewSize = null;
            specificPreviewSize = null;
            previewSize = null;
        }
    }

    private Camera.Size getBestSupportedSize(List<Camera.Size> sizes, Point previewViewSize) {
        if (sizes == null || sizes.size() == 0) {
            return mCamera.getParameters().getPreviewSize();
        }
        Camera.Size[] tempSizes = sizes.toArray(new Camera.Size[0]);
        Arrays.sort(tempSizes, new Comparator<Camera.Size>() {
            @Override
            public int compare(Camera.Size o1, Camera.Size o2) {
                if (o1.width > o2.width) {
                    return -1;
                } else if (o1.width == o2.width) {
                    return o1.height > o2.height ? -1 : 1;
                } else {
                    return 1;
                }
            }
        });
        sizes = Arrays.asList(tempSizes);

        Camera.Size bestSize = sizes.get(0);
        float previewViewRatio;
        if (previewViewSize != null) {
            previewViewRatio = (float) previewViewSize.x / (float) previewViewSize.y;
        } else {
            previewViewRatio = (float) bestSize.width / (float) bestSize.height;
        }

        if (previewViewRatio > 1) {
            previewViewRatio = 1 / previewViewRatio;
        }
        boolean isNormalRotate = (additionalRotation % 180 == 0);

        for (Camera.Size s : sizes) {
            if (specificPreviewSize != null && specificPreviewSize.x == s.width && specificPreviewSize.y == s.height) {
                return s;
            }
            if (isNormalRotate) {
                if (Math.abs((s.height / (float) s.width) - previewViewRatio) < Math.abs(bestSize.height / (float) bestSize.width - previewViewRatio)) {
                    bestSize = s;
                }
            } else {
                if (Math.abs((s.width / (float) s.height) - previewViewRatio) < Math.abs(bestSize.width / (float) bestSize.height - previewViewRatio)) {
                    bestSize = s;
                }
            }
        }
        return bestSize;
    }

    public List<Camera.Size> getSupportedPreviewSizes() {
        if (mCamera == null) {
            return null;
        }
        return mCamera.getParameters().getSupportedPreviewSizes();
    }

    public List<Camera.Size> getSupportedPictureSizes() {
        if (mCamera == null) {
            return null;
        }
        return mCamera.getParameters().getSupportedPictureSizes();
    }


    @Override
    public void onPreviewFrame(byte[] nv21, Camera camera) {
        if (cameraListener != null) {
            cameraListener.onPreview(nv21, camera);
        }
    }

    private TextureView.SurfaceTextureListener textureListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(SurfaceTexture surfaceTexture, int width, int height) {
//            start();
            if (mCamera != null) {
                try {
                    mCamera.setPreviewTexture(surfaceTexture);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        @Override
        public void onSurfaceTextureSizeChanged(SurfaceTexture surfaceTexture, int width, int height) {
            Log.i(TAG, "onSurfaceTextureSizeChanged: " + width + "  " + height);
        }

        @Override
        public boolean onSurfaceTextureDestroyed(SurfaceTexture surfaceTexture) {
            stop();
            return false;
        }

        @Override
        public void onSurfaceTextureUpdated(SurfaceTexture surfaceTexture) {

        }
    };
    private SurfaceHolder.Callback surfaceCallback = new SurfaceHolder.Callback() {
        @Override
        public void surfaceCreated(SurfaceHolder holder) {
//            start();
            if (mCamera != null) {
                try {
                    mCamera.setPreviewDisplay(holder);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        @Override
        public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

        }

        @Override
        public void surfaceDestroyed(SurfaceHolder holder) {
            stop();
        }
    };

    public void changeDisplayOrientation(int rotation) {
        if (mCamera != null) {
            this.rotation = rotation;
            displayOrientation = getCameraOri(rotation);
            mCamera.setDisplayOrientation(displayOrientation);
            if (cameraListener != null) {
                cameraListener.onCameraConfigurationChanged(mCameraId, displayOrientation);
            }
        }
    }
    public boolean switchCamera() {
        if (Camera.getNumberOfCameras() < 2) {
            return false;
        }
        // cameraId ,0为后置，1为前置
        specificCameraId = 1 - mCameraId;
        stop();
        start();
        return true;
    }

    public static final class Builder {

        /**
         * 预览显示的view，目前仅支持surfaceView和textureView
         */
        private View previewDisplayView;

        /**
         * 是否镜像显示，只支持textureView
         */
        private boolean isMirror;
        /**
         * 指定的相机ID
         */
        private Integer specificCameraId;
        /**
         * 事件回调
         */
        private CameraListener cameraListener;
        /**
         * 屏幕的长宽，在选择最佳相机比例时用到
         */
        private Point previewViewSize;
        /**
         * 传入getWindowManager().getDefaultDisplay().getRotation()的值即可
         */
        private int rotation;
        /**
         * 指定的预览宽高，若系统支持则会以这个预览宽高进行预览
         */
        private Point previewSize;

        /**
         * 额外的旋转角度（用于适配一些定制设备）
         */
        private int additionalRotation;

        public Builder() {
        }


        public Builder previewOn(View val) {
            if (val instanceof SurfaceView || val instanceof TextureView) {
                previewDisplayView = val;
                return this;
            } else {
                throw new RuntimeException("you must preview on a textureView or a surfaceView");
            }
        }


        public Builder isMirror(boolean val) {
            isMirror = val;
            return this;
        }

        public Builder previewSize(Point val) {
            previewSize = val;
            return this;
        }

        public Builder previewViewSize(Point val) {
            previewViewSize = val;
            return this;
        }

        public Builder rotation(int val) {
            rotation = val;
            return this;
        }

        public Builder additionalRotation(int val) {
            additionalRotation = val;
            return this;
        }

        public Builder specificCameraId(Integer val) {
            specificCameraId = val;
            return this;
        }

        public Builder cameraListener(CameraListener val) {
            cameraListener = val;
            return this;
        }

        public CameraHelper build() {
            if (previewViewSize == null) {
                Log.e(TAG, "previewViewSize is null, now use default previewSize");
            }
            if (cameraListener == null) {
                Log.e(TAG, "cameraListener is null, callback will not be called");
            }
            if (previewDisplayView == null) {
                throw new RuntimeException("you must preview on a textureView or a surfaceView");
            }
            return new CameraHelper(this);
        }
    }
}
```
