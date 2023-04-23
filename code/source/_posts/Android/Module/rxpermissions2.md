---
title: 权限管理
tags: 
    - 权限管理
categories: 
    - Android
description: 权限管理
date: 2020-03-25 09:07:46
updated: 2020-03-25 09:07:46
---

## 原生：权限动态申请

```java
public class PermissionUtl {
    private static String TAG = PermissionUtl.class.getSimpleName();

    public static void init(AppCompatActivity app) {
        // 前置权限申请
    }

    public static boolean request(AppCompatActivity app, int requestCode, String permission) {
        if (permission != null && permission.length() > 0) {
            try {
                if (Build.VERSION.SDK_INT >= 23) {
                    if (app.checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED) {
                        // 是否应该显示权限请求
                        app.shouldShowRequestPermissionRationale(permission);
                        app.requestPermissions(new String[]{permission}, requestCode);
                        Log.e(TAG, "requestPermissions: " + permission);
                        return true;
                    }
                } else {
                    if (ContextCompat.checkSelfPermission(app, permission) != PackageManager.PERMISSION_GRANTED) {
                        ActivityCompat.shouldShowRequestPermissionRationale(app, permission);
                        ActivityCompat.requestPermissions(app, new String[]{permission}, requestCode);
                        Log.e(TAG, "requestPermissions: " + permission);
                    }
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
        return false;
    }
}
requestPermissions(99, Manifest.permission.CAMERA);

// 申请结果通知函数：Activity回调
@Override
public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
    super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    if (grantResults.length > 0 && grantResults[0]==PackageManager.PERMISSION_GRANTED){
        // TODO：权限申请成功
    }else {
        Toast.makeText(this, "系统权限申请失败，功能无法使用", Toast.LENGTH_SHORT).show();
    }
}
```

## XXPermissions

+ [github](https://github.com/getActivity/XXPermissions)
  + 权限申请封装 - 一条语句搞定功能相关所有权限申请
+ [简书博文](https://www.jianshu.com/p/c69ff8a445ed)

+ settings.gradle

```gradle
dependencyResolutionManagement {
    repositories {
        // JitPack 远程仓库：https://jitpack.io
        maven { url 'https://jitpack.io' }
    }
}
```

+ build.gradle

```gradle
android {
    // 支持 JDK 1.8
    compileOptions {
        targetCompatibility JavaVersion.VERSION_1_8
        sourceCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    // 权限请求框架：https://github.com/getActivity/XXPermissions
    implementation 'com.github.getActivity:XXPermissions:18.0'
}
```

+ AndroidX 兼容, gradle.properties 文件添加项
```properties
# 表示将第三方库迁移到 AndroidX
android.enableJetifier = true
```

+ Android 10 分区存储特性, AndroidManifest.xml 中加入
```xml
<manifest>
    <application>
        <!-- 告知 XXPermissions 当前项目已经适配了分区存储特性 -->
        <meta-data
            android:name="ScopedStorage"
            android:value="true" />
    </application>
</manifest>
```

+ Java应用示例

```java
XXPermissions.with(this)
        // 申请单个权限
        .permission(Permission.RECORD_AUDIO)
        // 申请多个权限
        .permission(Permission.Group.CALENDAR)
        // 设置权限请求拦截器（局部设置）
        //.interceptor(new PermissionInterceptor())
        // 设置不触发错误检测机制（局部设置）
        //.unchecked()
        .request(new OnPermissionCallback() {

            @Override
            public void onGranted(@NonNull List<String> permissions, boolean allGranted) {
                if (!allGranted) {
                    toast("获取部分权限成功，但部分权限未正常授予");
                    return;
                }
                toast("获取录音和日历权限成功");
            }

            @Override
            public void onDenied(@NonNull List<String> permissions, boolean doNotAskAgain) {
                if (doNotAskAgain) {
                    toast("被永久拒绝授权，请手动授予录音和日历权限");
                    // 如果是被永久拒绝就跳转到应用权限系统设置页面
                    XXPermissions.startPermissionActivity(context, permissions);
                } else {
                    toast("获取录音和日历权限失败");
                }
            }
        });
```

## hipermission

```gradle
    implementation 'me.weyye.hipermission:library:1.0.7'
```

### hipermission - 应用

+ [GitHub](https://github.com/AboutAndroid/HiPermission)

## rxpermissions2

+ [GitHub](https://github.com/tbruyelle/RxPermissions)

```gradle
    // 基于rxjava3版本
    implementation 'io.reactivex.rxjava3:rxandroid:3.0.2'
    implementation 'io.reactivex.rxjava3:rxjava:3.1.6'
    implementation 'com.github.tbruyelle:rxpermissions:0.12'

    allprojects {
        repositories {
            ...
            maven { url 'https://jitpack.io' }
        }
    }

    dependencies {
        implementation 'com.github.tbruyelle:rxpermissions:0.12'
    }
    // import com.tbruyelle.rxpermissions3.RxPermissions;
```

### rxpermissions2 - 简单应用

```java
RxPermissions rxPermission = new RxPermissions(MyActivity.this);
//请求权限全部结果
rxPermissions
    .request(Manifest.permission.CAMERA)
    .subscribe(granted -> {
        if (granted) { // Always true pre-M
           // I can control the camera now
        } else {
           // Oups permission denied
        }
    });
rxPermissions
    .request(Manifest.permission.CAMERA,
             Manifest.permission.READ_PHONE_STATE)
    .subscribe(granted -> {
        if (granted) {
           // All requested permissions are granted
        } else {
           // At least one permission is denied
        }
    });
// 分别请求权限
rxPermissions
    .requestEach(Manifest.permission.CAMERA,
             Manifest.permission.READ_PHONE_STATE)
    .subscribe(permission -> { // will emit 2 Permission objects
        if (permission.granted) {
           // `permission.name` is granted !
        } else if (permission.shouldShowRequestPermissionRationale) {
           // Denied permission without ask never again
        } else {
           // Denied permission with ask never again
           // Need to go to the settings
        }
    });
rxPermissions
    .requestEachCombined(Manifest.permission.CAMERA,
             Manifest.permission.READ_PHONE_STATE)
    .subscribe(permission -> { // will emit 1 Permission object
        if (permission.granted) {
           // All permissions are granted !
        } else if (permission.shouldShowRequestPermissionRationale) {
           // At least one denied permission without ask never again
        } else {
           // At least one denied permission with ask never again
           // Need to go to the settings
        }
    });
```
