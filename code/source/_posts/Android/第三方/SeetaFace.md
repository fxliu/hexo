---
title: SeetaFace
tags: 
    - SeetaFace
categories: 
    - Android
description: SeetaFace
date: 2022-07-25 22:02:12
updated: 2022-07-25 22:02:12
---

## SeetaFace

* SeetaFace2
* https://github.com/seetaface/SeetaFaceEngine
* https://github.com/seetaface/SeetaFaceEngine2
* https://github.com/seetafaceengine/SeetaFace2
  * https://github.com/xiaoxiaoazhang/SeetaFace2AndroidDemo
* https://github.com/seetafaceengine/SeetaFace6
* https://github.com/SeetaFace6Open/SeetaFace6JNI
* http://leanote.com/blog/post/5e7d6cecab64412ae60016ef

```sh
cd /d %~dp0\SeetaFace\index-master\OpenRoleZoo\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\TenniS\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\SeetaAuthorize\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\FaceAntiSpoofingX6\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\FaceBoxes\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\FaceRecognizer6\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\FaceTracker6\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\Landmarker\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\PoseEstimator6\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\QualityAssessor3\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\SeetaAgePredictor\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\SeetaEyeStateDetector\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\SeetaGenderPredictor\craft
build.win.vc14.all.cmd

cd /d %~dp0\SeetaFace\index-master\SeetaMaskDetector\craft
build.win.vc14.all.cmd
```

````
@set pwd=%~dp0

@if not exist %pwd%build\ md %pwd%build\
@if not exist %pwd%build\arm64-v8a\ md %pwd%build\arm64-v8a\
@if not exist %pwd%build\armeabi-v7a\ md %pwd%build\armeabi-v7a\

@call:build %pwd% OpenRoleZoo libORZ_static.a
@call:build %pwd% SeetaAuthorize libStAuthorize.so
@call:build %pwd% TenniS libtennis.so
@call:build %pwd% FaceBoxes\FaceDetector libStDetector600.so
@call:build %pwd% FaceTracker6\FaceTracking libStTracking600.so
@call:build %pwd% FaceRecognizer6\FaceRecognizer libStRecognizer610.so
@call:build %pwd% Landmarker\Landmarker libStLandmarker600.so

@exit /B 1

:build
@set pwd=%~1
@set pro=%pwd%%~2
@set fn=%~3
cd /d %pro%\android\jni\
@echo ----------------%pro%----------------
@call D:\Android\Sdk\ndk\21.4.7075529\ndk-build.cmd clean
@call D:\Android\Sdk\ndk\21.4.7075529\ndk-build.cmd -j16
@copy /Y %pro%\android\obj\local\arm64-v8a\%fn% %pwd%build\arm64-v8a\
@copy /Y %pro%\android\obj\local\armeabi-v7a\%fn% %pwd%build\armeabi-v7a\
@cd /d %pwd%
:: 函数结束标记
goto:eof
```

cd /d %~dp0\SeetaFace\index-master\FaceAntiSpoofingX6\FaceAntiSpoofingX\android\jni
cd /d %~dp0\SeetaFace\index-master\PoseEstimator6\PoseEstimation\android\jni
cd /d %~dp0\SeetaFace\index-master\QualityAssessor3\QualityAssessor\android\jni
cd /d %~dp0\SeetaFace\index-master\SeetaAgePredictor\AgePredictor\android\jni
cd /d %~dp0\SeetaFace\index-master\SeetaEyeStateDetector\EyeStateDetector\android\jni
cd /d %~dp0\SeetaFace\index-master\SeetaGenderPredictor\GenderPredictor\android\jni
cd /d %~dp0\SeetaFace\index-master\SeetaMaskDetector\MaskDetector\android\jni
````

## 模型设置

```c++
SeetaModelSetting setting;
setting.device = SEETA_DEVICE_CPU;
setting.id = 0;
setting.model = {"fr_model.csta", NULL};
// C++封装：默认SEETA_DEVICE_CPU
class seeta::ModelSetting : SeetaModelSetting;
seeta::ModelSetting setting;
setting.append("fr_model.csta");
```

## 人脸识别器

```C++
seeta::FaceRecognizer FR(setting);
// 线程安全
1. 对象可以跨线程传递。线程1构造的识别器，可以在线程2中调用。
2. 对象的构造可以并发构造，即可以多个线程同时构造识别器。
3. 单个对象的接口调用不可以并发调用，即单个对象，在多个线程同时使用是被禁止的。
当然一些特殊的对象会具有更高级别的线程安全级别，例如seeta::FaceDatabase的接口调用就可以并发调用，但是计算不会并行。
```

## 人脸检测

```C++
// 构造检测器
#include <seeta/FaceDetector.h>
seeta::FaceDetector *new_fd() {
    seeta::ModelSetting setting;
    setting.append("face_detector.csta");
    return new seeta::FaceDetector(setting);
}
// 检测器常规属性
seeta::FaceDetector::PROPERTY_MIN_FACE_SIZE     最小人脸；默认值为20，单位像素
seeta::FaceDetector::PROPERTY_THRESHOLD         检测器阈值；默认值是0.9，合理范围为[0, 1]
seeta::FaceDetector::PROPERTY_MAX_IMAGE_WIDTH   可检测的图像最大宽度；默认值都是2000
seeta::FaceDetector::PROPERTY_MAX_IMAGE_HEIGHT  可检测的图像最大高度；默认值都是2000
    
// 检测：输入图片，输出4角定位以及可信度
#include <seeta/FaceDetector.h>
void detect(seeta::FaceDetector *fd, const SeetaImageData &image) {
    std::vector<SeetaFaceInfo> faces = fd->detect_v2(image);
    for (auto &face : faces) {
        SeetaRect rect = face.pos;
        std::cout << "[" << rect.x << ", " << rect.y << ", "
                  << rect.width << ", " << rect.height << "]: "
                  << face.score << std::endl;
    }
}
// 最大人脸快速排序
std::partial_sort(faces.begin(), faces.begin() + 1, faces.end(), [](SeetaFaceInfo a, SeetaFaceInfo b) {
    return a.pos.width > b.pos.width;
});
```

## 人脸关键点定位(5点)

```C++
// 构造定位器
#include <seeta/FaceLandmarker.h>
seeta::FaceLandmarker *new_fl() {
    seeta::ModelSetting setting;
    setting.append("face_landmarker_pts5.csta");
    return new seeta::FaceLandmarker(setting);
}
// 人脸关键点定位: 需要传入原始图像和人脸位置
#include <seeta/FaceLandmarker.h>
void mark(seeta::FaceLandmarker *fl, const SeetaImageData &image, const SeetaRect &face) {
    std::vector<SeetaPointF> points = fl->mark(image, face);
    for (auto &point : points) {
        std::cout << "[" << point.x << ", " << point.y << "]" << std::endl;
    }
}
```

## 人脸特征提取和对比

```c++
// 这里SeetaFace的特征都是float数组，特征对比方式是向量內积
// 构造器
#include <seeta/FaceRecognizer.h>
seeta::FaceRecognizer *new_fr() {
    seeta::ModelSetting setting;
    setting.append("face_recognizer.csta");
    return new seeta::FaceRecognizer(setting);
}
// 特征提取: 裁剪提取一体
#include <seeta/FaceRecognizer.h>
#include <memory>
std::shared_ptr<float> extract(
        seeta::FaceRecognizer *fr,
        const SeetaImageData &image,
        const std::vector<SeetaPointF> &points) {
    // 使用GetExtractFeatureSize获取当前模型特征长度
    std::shared_ptr<float> features(
        new float[fr->GetExtractFeatureSize()],
        std::default_delete<float[]>());
    // points是5点定位检测结果
    // image -> 基于关键点裁剪 -> 裁剪后图片提取特征
    fr->Extract(image, points.data(), features.get());
    return features;
}
// 特征提取：裁剪提取分开
std::shared_ptr<float> extract_v2(
        seeta::FaceRecognizer *fr,
        const SeetaImageData &image,
        const std::vector<SeetaPointF> &points) {
    std::shared_ptr<float> features(
        new float[fr->GetExtractFeatureSize()],
        std::default_delete<float[]>());
    seeta::ImageData face = fr->CropFaceV2(image, points.data());
    fr->ExtractCroppedFace(face, features.get());
    return features;
}
// 相似度计算: 相似度范围 [0, 1]
#include <seeta/FaceRecognizer.h>
#include <memory>
float compare(seeta::FaceRecognizer *fr,
        const std::shared_ptr<float> &feat1,
        const std::shared_ptr<float> &feat2) {
    return fr->CalculateSimilarity(feat1.get(), feat2.get());
}
```
