---
title: Service
tags: 
    - Service
categories: 
    - Android
description: Service
date: 2020-02-08 19:18:01
updated: 2020-02-08 19:18:01
---

## 基础

```xml
<!--AndroidManifest.xml：<activity> 同级注册服务-->
<service android:name=".MyService" />
<activity .../>
```

```java
// MyService.java
public class EsService extends Service {

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        Log.e("test", "onBind");
        return null;
    }
    @Override
    public void onCreate() {
        Log.e("test", "onCreate");
        super.onCreate();
    }
    @Override
    public int onStartCommand(final Intent intent, int flags, int startId) {
        Log.e("test", "onStartCommand");
        Toast.makeText(this, "服务已经启动", Toast.LENGTH_LONG).show();
        // 参数
        String action = intent.getAction();
        boolean debug = intent.getStringExtra("DEBUG");

        return super.onStartCommand(intent, flags, startId);
    }
    @Override
    public void onDestroy() {
        Log.e("test", "onDestroy");
        super.onDestroy();
    }
}
```

```java
// 启动
Intent intent = new Intent(this, MyService.class);
// 指令
intent.setAction("START_READ_IDCARD");
// 参数
intent.putExtra("DEBUG", true);
startService(intent);
```
