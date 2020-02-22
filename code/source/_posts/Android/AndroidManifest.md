---
title: AndroidManifest
tags: 
    - AndroidManifest
categories: 
    - Android
description: AndroidManifest
date: 2020-02-14 12:20:58
updated: 2020-02-14 12:20:58
---

## 权限

```xml
<manifest>
    <!-- NFC权限 -->
    <uses-permission android:name="android.permission.NFC" />
    <!-- 声明所依赖的外部的硬件，并指定为必须 -->
    <uses-feature
        android:name="android.hardware.nfc"
        android:required="true" />
    <!-- 网络权限 -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <application />
</manifest>
```

### 权限动态申请

```java
// 方式1
if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
    // 申请权限
    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA}, Constant.REQ_PERM_CAMERA);
    return;
}
// 方式2
public void requestPermissions(int requestCode, String permission) {
    if (permission != null && permission.length() > 0) {
        try {
            if (Build.VERSION.SDK_INT >= 23) {
                // 检查是否有权限
                int hasPer = checkSelfPermission(permission);
                if (hasPer != PackageManager.PERMISSION_GRANTED) {
                    // 显示权限请求
                    shouldShowRequestPermissionRationale(permission);
                    requestPermissions(new String[]{permission}, requestCode);
                    Log.e(TAG, "requestPermissions: " + permission);
                }
            } else {

            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
// 99是指用户点击取消后继续提醒次数
requestPermissions(99, Manifest.permission.CAMERA);

// 申请结果通知函数
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

### debug状态

```java
boolean isDebug(Context context) {
    try {
        ApplicationInfo info = context.getApplicationInfo();
        return (info.flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0;
    } catch (Exception e) {
        return false;
    }
}
```
