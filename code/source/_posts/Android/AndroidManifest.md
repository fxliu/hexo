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
if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
    // 申请权限
    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA}, Constant.REQ_PERM_CAMERA);
    return;
}
```
