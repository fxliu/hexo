---
title: BroadcastReceiver
tags: 
    - BroadcastReceiver
categories: 
    - Android
description: BroadcastReceiver
date: 2022-08-03 20:12:12
updated: 2022-08-03 20:12:12
---

## BroadcastReceiver

Android 四大组件之一，系统广播

## 接收

```xml
<manifest ...>
    <application ...>
        <!-- Android系统重启广播接收 -->
        <receiver
            android:name=".BootBroadcastReceiver">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </receiver>
    </application>
</manifest>
```

```java
// adb root - 部分机器不允许发BOOT_COMPLETED消息, root下就好了
// adb shell
// am broadcast -a android.intent.action.BOOT_COMPLETED -n com.eseid.eid_idcard_svr/com.eseid.eid_idcard_svr.BootBroadcastReceiver
public class BootBroadcastReceiver extends BroadcastReceiver {
    private static final String TAG = BootBroadcastReceiver.class.getSimpleName();

    @Override
    public void onReceive(Context context, Intent intent) {
        // 收到重启消息
        Log.d(intent.getAction());
    }
}
```
