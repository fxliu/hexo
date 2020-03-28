---
title: PictureSelector
tags: 
    - PictureSelector
categories: 
    - Android
description: PictureSelector
date: 2020-03-28 19:30:25
updated: 2020-03-28 19:30:25
---

## 图片选择器

+ [PictureSelector](https://github.com/LuckSiege/PictureSelector)
  + 相机 + 相册 + 多种主题
  + 持续更新
+ [图片选择器](https://github.com/qingmei2/RxImagePicker)
  + 响应式图片选择器，支持相机+相册， 灵活应用于各种需求嵌入
  + 知乎主题 + 微信主题

## PictureSelector

```Java
public class PictureUtil {
    private static String TAG = PictureUtil.class.getSimpleName();
    private static JsInterface mJsInterface;
    public static void init(JsInterface jsInterface){
        mJsInterface = jsInterface;
    }
    public static void startPicture(AppCompatActivity app, JsonObject jsonObject) {
        start(app, jsonObject, PictureConfig.CHOOSE_REQUEST);
    }
    public static void startCamera(AppCompatActivity app, JsonObject jsonObject) {
        start(app, jsonObject, PictureConfig.REQUEST_CAMERA);
    }
    public static void onResult(AppCompatActivity app, Intent intent) {
    }
    // --------------------------------------------------------------------------
    private static void start(AppCompatActivity app, JsonObject jsonObject, final int requestCode) {
        JsonUtil js = new JsonUtil(jsonObject);
        String strTheme = js.value("theme", "default");
        PictureParameterStyle parameterStyle = getPictureParameterStyle(app, strTheme);
        PictureCropParameterStyle cropParameterStyle = getCropStyle(app, parameterStyle, strTheme);

        PictureSelectionModel pictureSelectionModel;
        // 全部.PictureMimeType.ofAll()、图片.ofImage()、视频.ofVideo()、音频.ofAudio()
        if(requestCode == PictureConfig.REQUEST_CAMERA)
            pictureSelectionModel = PictureSelector.create(app)
                    .openCamera(getMode(js.value("mode", "image")));
        else
            pictureSelectionModel = PictureSelector.create(app)
                    .openGallery(getMode(js.value("mode", "image")));
        pictureSelectionModel
                // 外部传入图片加载引擎，必传项
                .loadImageEngine(GlideEngine.createGlideEngine())
                // 主题样式设置 具体参考 values/styles
                .theme(getTheme(strTheme))
                // 是否开启微信图片选择风格
                .isWeChatStyle(isWeChat(strTheme))
                // 动态自定义相册主题
                .setPictureStyle(parameterStyle)
                // 动态自定义裁剪主题
                .setPictureCropStyle(cropParameterStyle)
                // 自定义相册启动退出动画
                .setPictureWindowAnimationStyle(getPictureWindowAnimationStyle(js.value("animation_style", "default")))
                // 图片和视频是否可以同选,只在ofAll模式下有效
                .isWithVideoImage(true)
                // 图片选择数量
                .maxSelectNum(js.value("max_select_num", 5))
                .minSelectNum(js.value("min_select_num", 1))
                // 视频选择数量, 如果没有单独设置的需求则可以不设置，同用 图片选择数量
                // .maxVideoSelectNum(1)
                // .minVideoSelectNum(1)
                .imageSpanCount(js.value("span_count", 4))
                // 未选择数据时点击按钮是否可以返回
                .isReturnEmpty(false)
                // 设置相册Activity方向，不设置默认使用系统
                // .setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED)
                // 是否显示原图控制按钮，如果设置为true则用户可以自由选择是否使用原图，压缩、裁剪功能将会失效
                .isOriginalImageControl(js.value("original", false))
                // 重命名拍照文件名、如果是相册拍照则内部会自动拼上当前时间戳防止重复
                // 注意这个只在使用相机时可以使用，如果使用相机又开启了压缩或裁剪 需要配合压缩和裁剪文件名api
                //.cameraFileName(System.currentTimeMillis() +".jpg")
                // 重命名压缩文件名、 注意这个不要重复，只适用于单张图压缩使用
                //.renameCompressFile(System.currentTimeMillis() +".jpg")
                // 重命名裁剪文件名、 注意这个不要重复，只适用于单张图裁剪使用
                //.renameCropFileName(System.currentTimeMillis() + ".jpg")
                .selectionMode(js.value("single", true) ? PictureConfig.SINGLE : PictureConfig.MULTIPLE)
                // 单选模式下是否直接返回，PictureConfig.SINGLE模式下有效
                .isSingleDirectReturn(js.value("single_direct_return", false))
                // 是否可预览图片
                .previewImage(js.value("preview_img", true))
                // 是否可预览视频
                .previewVideo(js.value("preview_video", true))
                // 是否可播放音频
                .enablePreviewAudio(js.value("preview_audio", true))
                // 是否显示拍照按钮
                .isCamera(js.value("camera", true))
                // 多图裁剪时是否支持跳过，默认支持
                .isMultipleSkipCrop(js.value("multiple_skip_crop", true))
                // 多图裁剪底部列表显示动画效果
                .isMultipleRecyclerAnimation(true)
                // 图片列表点击 缩放效果 默认true
                .isZoomAnim(true)
                // 拍照保存图片格式后缀,默认jpeg
                .imageFormat(PictureMimeType.PNG)
                // 是否压缩
                .compress(js.value("compress", true))// 是否压缩
                // 图片压缩后输出质量 0~ 100
                .compressQuality(js.value("compress_quality", 80))
                //同步true或异步false 压缩 默认同步
                .synOrAsy(true)
                .minimumCompressSize(js.value("min_compress_size", 100))// 小于100kb的图片不压缩
                //.queryMaxFileSize(10)// 只查多少M以内的图片、视频、音频  单位M
                //.compressSavePath(getPath())//压缩图片保存地址
                // 是否显示gif图片
                .isGif(js.value("gif", false))

                // 是否裁剪
                .enableCrop(js.value("crop", true))
                // 裁剪比例 如16:9 3:2 3:4 1:1 可自定义
                .withAspectRatio(js.value("aspect_ratio_x", 3), js.value("aspect_ratio_y", 2))
                // 裁剪框是否可拖拽
                .freeStyleCropEnabled(js.value("free_crop", true))
                // 是否圆形裁剪
                .circleDimmedLayer(js.value("crop_circular", false))
                // 设置圆形裁剪背景色值
                // .setCircleDimmedColor(ContextCompat.getColor(app, R.color.app_color_white))
                // 设置圆形裁剪边框色值
                // .setCircleDimmedBorderColor(ContextCompat.getColor(app, R.color.app_color_red))
                // 设置圆形裁剪边框粗细
                .setCircleStrokeWidth(js.value("crop_circular", 3))
                // 是否显示裁剪矩形边框 圆形裁剪时建议设为false
                .showCropFrame(js.value("crop_frame", true))
                // 是否显示裁剪矩形网格 圆形裁剪时建议设为false
                .showCropGrid(js.value("crop_grid", true))
                // .cutOutQuality(90)// 裁剪输出质量 默认100
                //.cropWH()// 裁剪宽高比，设置如果大于图片本身宽高则无效
                //.cropImageWideHigh()// 裁剪宽高比，设置如果大于图片本身宽高则无效
                .rotateEnabled(js.value("rotate", true)) // 裁剪是否可旋转图片
                .scaleEnabled(js.value("scale", true)) // 裁剪是否可旋转图片

                // 是否开启点击声音
                .openClickSound(js.value("voice", true))
                // 是否可拖动裁剪框(固定)
                .isDragFrame(js.value("drag_frame", true))
                // 视频声音范围
                .videoMinSecond(js.value("video_min_second", 5))
                .videoMaxSecond(js.value("video_max_second", 15))
                // 录制视频秒数 默认60s
                .recordVideoSecond(js.value("video_second", 60))
                // .videoQuality(1)// 视频录制质量 0 or 1
                // 预览图片时 是否增强左右滑动图片体验(图片滑动一半即可看到上一张是否选中)
                .previewEggs(true)

                // 结果回调 onActivityResult
                // .forResult(PictureConfig.CHOOSE_REQUEST);
                .forResult(requestCode, new OnResultCallbackListener() {
                    @Override
                    public void onResult(List<LocalMedia> result) {
                        JsonArray objs = new JsonArray();
                        for (LocalMedia media : result) {
                            // 裁剪+压缩情况：裁剪和压缩反馈结果是一个
                            Log.i(TAG, "是否压缩:" + media.isCompressed());
                            Log.i(TAG, "压缩:" + media.getCompressPath());
                            Log.i(TAG, "原图:" + media.getPath());
                            Log.i(TAG, "是否裁剪:" + media.isCut());
                            Log.i(TAG, "裁剪:" + media.getCutPath());
                            Log.i(TAG, "是否开启原图:" + media.isOriginal());
                            Log.i(TAG, "原图路径:" + media.getOriginalPath());
                            Log.i(TAG, "Android Q 特有Path:" + media.getAndroidQToPath());

                            String strFile = "";
                            if(media.isCompressed())
                                strFile = media.getCompressPath();
                            else if(media.isCut())
                                strFile = media.getCutPath();
                            else if(media.isOriginal())
                                strFile = media.getOriginalPath();
                            if(strFile.isEmpty())
                                strFile = media.getPath();

                            JsonObject obj = new JsonObject();
                            Bitmap bitmap = BitmapUtils.loadBitmapFromFile(app, strFile);
                            obj.addProperty("path", strFile);
                            obj.addProperty("base64", BitmapUtils.bitmapToJpegBase64(bitmap, 100, 400));
                            objs.add(obj);
                        }
                        if(requestCode == PictureConfig.REQUEST_CAMERA)
                            mJsInterface.sendCameraSuccess(objs.toString());
                        else
                            mJsInterface.sendPictureSuccess(objs.toString());
                    }
                    @Override
                    public void onCancel() {
                        Log.i(TAG, "PictureSelector Cancel");
                        if(requestCode == PictureConfig.REQUEST_CAMERA)
                            mJsInterface.sendCameraError("Cancel");
                        else
                            mJsInterface.sendPictureError("Cancel");
                    }
                });
    }
    // ---------------------------------------------------------------------------
    // 参数
    private static int getMode(String strMode) {
        switch (strMode) {
            case "all":
                return PictureMimeType.ofAll();
            case "video":
                return PictureMimeType.ofVideo();
            case "audio":
                return PictureMimeType.ofAudio();
            case "image":
            default:
                return PictureMimeType.ofImage();
        }
    }
    private static int getTheme(String strTheme) {
        switch (strTheme) {
            case "white":
                return R.style.picture_white_style;
            case "qq":
                return R.style.picture_QQ_style;
            case "sina":
                return R.style.picture_Sina_style;
            case "wx":
                return R.style.picture_WeChat_style;
            case "default":
            default:
                return R.style.picture_default_style;
        }
    }
    private static boolean isWeChat(String strTheme) {
        return strTheme.equals("chat");
    }
    private static PictureParameterStyle getPictureParameterStyle(AppCompatActivity app, String strTheme) {
        switch (strTheme) {
            case "white":
                return getWhiteStyle(app);
            case "qq":
                return getNumStyle(app);
            case "sina":
                return getSinaStyle(app);
            case "wx":
                return getWeChatStyle(app);
            case "default":
            default:
                return getDefaultStyle(app);
        }
    }
    private static PictureCropParameterStyle getCropStyle(AppCompatActivity app, PictureParameterStyle style, String strTheme) {
        switch (strTheme) {
            case "white":
                return getWhiteCropStyle(app, style);
            case "qq":
                return getNumCropStyle(app, style);
            case "sina":
                return getSinaCropStyle(app, style);
            case "wx":
                return getWeChatCropStyle(app, style);
            case "default":
            default:
                return getDefaultCropStyle(app, style);
        }
    }
    // -----------------------------------------------------------------
    // 相册弹出动画
    private static PictureWindowAnimationStyle getPictureWindowAnimationStyle(String style) {
        PictureWindowAnimationStyle animationStyle = new PictureWindowAnimationStyle();
        if(style.equals("up"))
            animationStyle.ofAllAnimation(R.anim.picture_anim_up_in, R.anim.picture_anim_down_out);
        return animationStyle;
    }
    // -----------------------------------------------------------------
    // 主题
    private static PictureParameterStyle getDefaultStyle(AppCompatActivity app) {
        // 相册主题：从源码Demo中 获取即可
        PictureParameterStyle pictureParameterStyle = new PictureParameterStyle();
        return pictureParameterStyle;
    }
    private static PictureCropParameterStyle getDefaultCropStyle(AppCompatActivity app, PictureParameterStyle pictureParameterStyle) {
        return new PictureCropParameterStyle(
                ContextCompat.getColor(app, R.color.app_color_grey),
                ContextCompat.getColor(app, R.color.app_color_grey),
                Color.parseColor("#393a3e"),
                ContextCompat.getColor(app, R.color.app_color_white),
                pictureParameterStyle.isChangeStatusBarFontColor);
    }
    private static PictureParameterStyle getWhiteStyle(AppCompatActivity app) {
        // 相册主题：从源码Demo中 获取即可
    }
    private static PictureCropParameterStyle getWhiteCropStyle(AppCompatActivity app, PictureParameterStyle pictureParameterStyle) {
        // 相册主题：从源码Demo中 获取即可
    }
    private static PictureParameterStyle getNumStyle(AppCompatActivity app) {
        // 相册主题：从源码Demo中 获取即可
    }
    private static PictureCropParameterStyle getNumCropStyle(AppCompatActivity app, PictureParameterStyle pictureParameterStyle) {
        // 相册主题：从源码Demo中 获取即可
    }
    private static PictureParameterStyle getSinaStyle(AppCompatActivity app) {
        // 相册主题：从源码Demo中 获取即可
    }
    private static PictureCropParameterStyle getSinaCropStyle(AppCompatActivity app, PictureParameterStyle pictureParameterStyle) {
        // 相册主题：从源码Demo中 获取即可
    }
    private static PictureParameterStyle getWeChatStyle(AppCompatActivity app) {
        // 相册主题：从源码Demo中 获取即可
    }
    private static PictureCropParameterStyle getWeChatCropStyle(AppCompatActivity app, PictureParameterStyle pictureParameterStyle) {
        // 相册主题：从源码Demo中 获取即可
    }
}

```
