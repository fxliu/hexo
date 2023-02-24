---
title: Toaster
tags: 
    - Toaster
categories: 
    - Android
description: Toaster
date: 2023-02-24 14:31:09
updated: 2023-02-24 14:31:09
---

## 吐司框架

+ [github](https://github.com/getActivity/Toaster)

```gradle
// Gradle 配置是在 7.0 以下, build.gradle
allprojects {
    repositories {
        // JitPack 远程仓库：https://jitpack.io
        maven { url 'https://jitpack.io' }
    }
}
// Gradle 配置是 7.0 及以上, settings.gradle
dependencyResolutionManagement {
    repositories {
        // JitPack 远程仓库：https://jitpack.io
        maven { url 'https://jitpack.io' }
    }
}

android {
    // 支持 JDK 1.8
    compileOptions {
        targetCompatibility JavaVersion.VERSION_1_8
        sourceCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    // 吐司框架：https://github.com/getActivity/Toaster
    implementation 'com.github.getActivity:Toaster:12.0'
}
```

### 吐司框架 - 基础应用

```java
// 初始化
public class XxxApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();

        // 初始化 Toast 框架
        Toaster.init(this);
    }
}
// 应用
// 显示 Toast
Toaster.show(CharSequence text);
Toaster.show(int id);
Toaster.show(Object object);

// debug 模式下显示 Toast
Toaster.debugShow(CharSequence text);
Toaster.debugShow(int id);
Toaster.debugShow(Object object);

// 延迟显示 Toast
Toaster.delayedShow(CharSequence text, long delayMillis);
Toaster.delayedShow(int id, long delayMillis);
Toaster.delayedShow(Object object, long delayMillis);

// 显示短 Toast
Toaster.showShort(CharSequence text);
Toaster.showShort(int id);
Toaster.showShort(Object object);

// 显示长 Toast
Toaster.showLong(CharSequence text);
Toaster.showLong(int id);
Toaster.showLong(Object object);

// 自定义显示 Toast
Toaster.show(ToastParams params);

// 取消 Toast
Toaster.cancel();

// 设置 Toast 布局（全局生效）
Toaster.setView(int id);

// 设置 Toast 样式（全局生效）
Toaster.setStyle(IToastStyle<?> style);
// 获取 Toast 样式
Toaster.getStyle()

// 判断当前框架是否已经初始化
Toaster.isInit();

// 设置 Toast 策略（全局生效）
Toaster.setStrategy(IToastStrategy strategy);
// 获取 Toast 策略
Toaster.getStrategy();

// 设置 Toast 重心和偏移
Toaster.setGravity(int gravity);
Toaster.setGravity(int gravity, int xOffset, int yOffset);

// 设置 Toast 拦截器（全局生效）
Toaster.setInterceptor(IToastInterceptor interceptor);
// 获取 Toast 拦截器
Toaster.getInterceptor();
```
