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

## 基础属性

```xml
<!-- android:icon 应用图标 -->
<!-- android:label 应用名称 -->
<!-- android:theme 样式，定义默认颜色，沉浸式状态栏等 -->
<application
    android:allowBackup="true"
    android:icon="@drawable/ic_launcher"
    android:label="@string/app_name"
    android:theme="@style/AppTheme" >
    <!-- android:name 窗口类：Java类绝对/相对路径 -->
    <!-- android:label 窗口名：标题栏显示文字 -->
    <activity
        android:name=".MainActivity"
        android:label="@string/app_name" >
        <intent-filter>
            <!-- 指定为入口窗体 -->
            <action android:name="android.intent.action.MAIN" />
            <!-- 指定应用要在Android系统应用列表中显示（只能指定一个） -->
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
</application>
```

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
