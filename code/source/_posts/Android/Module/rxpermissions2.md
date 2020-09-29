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

+ build.gradle -> buildscript.repositories / allprojects.repositories
  + `maven { url 'https://jitpack.io' }`
+ build.gradle -> dependencies
  + `implementation 'com.github.tbruyelle:rxpermissions:0.12'`

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

## rxpermissions2

`implementation 'com.tbruyelle.rxpermissions2:rxpermissions:0.9.4@aar'`

### rxpermissions2 - 简单应用

```java
public class ZPermissionUtil {
    private RxPermissions rxPermissions;
    private ZPermissionUtil() {}

    private static class RxPermissionUtilHolder {
        private static final ZPermissionUtil mInstance = new ZPermissionUtil();
    }

    public static ZPermissionUtil getInstance() {
        return RxPermissionUtilHolder.mInstance;
    }

    public void init(Activity activity) {
        rxPermissions = new RxPermissions(activity);
    }

    @SuppressLint("CheckResult")
    public void requestPermissions(final IPermissionsListener listener, final String... permissions) {
        if (listener == null)
            throw new RuntimeException("IPermissionsListener not null");
        rxPermissions.request(permissions)
                .subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Consumer<Boolean>() {
                    @Override
                    public void accept(Boolean aBoolean) throws Exception {
                        if (aBoolean) {
                            listener.onPermissionsSuccess();
                        } else {
                            listener.onPermissionsFail();
                        }
                    }
                });
    }

    public Observable<Boolean> requestPermissions(final String... permissions) {
        return rxPermissions.request(permissions);
    }

    public boolean isPermissions(String permission) {
        return rxPermissions.isGranted(permission);
    }
}
```

```java
RxPermissions rxPermission = new RxPermissions(FlashActivity.this);
//请求权限全部结果
rxPermission.request(
        Manifest.permission.CAMERA,
        Manifest.permission.READ_PHONE_STATE,
        Manifest.permission.WRITE_EXTERNAL_STORAGE,
        Manifest.permission.READ_EXTERNAL_STORAGE,
        Manifest.permission.ACCESS_COARSE_LOCATION)
        .subscribe(new Consumer<Boolean>() {
            @Override
            public void accept(Boolean granted) throws Exception {
                if (!granted) {
                    ToastUtils.showToast("App未能获取全部需要的相关权限，部分功能可能不能正常使用.");
                }
                //不管是否获取全部权限，进入主页面
                initCountDown();
            }
        });
// 分别请求权限
rxPermission.requestEach(
        Manifest.permission.CAMERA,
        Manifest.permission.READ_PHONE_STATE,
        Manifest.permission.WRITE_EXTERNAL_STORAGE,
        Manifest.permission.READ_EXTERNAL_STORAGE,
        Manifest.permission.ACCESS_COARSE_LOCATION)
        .subscribe(new Consumer<Permission>() {
            @Override
            public void accept(Permission permission) throws Exception {
                if (permission.granted) {
                    // 用户已经同意该权限
                    Log.d(TAG, permission.name + " is granted.");
                } else if (permission.shouldShowRequestPermissionRationale) {
                    // 用户拒绝了该权限，没有选中『不再询问』(Never ask again)
                    // 那么下次再次启动时，还会提示请求权限的对话框
                    Log.d(TAG, permission.name + " is denied. More info should be provided.");
                } else {
                    // 用户拒绝了该权限，并且选中『不再询问』
                    Log.d(TAG, permission.name + " is denied.");
                }
            }
        });
```
