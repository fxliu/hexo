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

## 静态注册 + 接收

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

## 动态注册+接收

```java
public final class EidMsg extends BroadcastReceiver {
    private static final String TAG = EidMsg.class.getSimpleName();
    // 自定义消息Action
    private static final String ACTION_LOG = "com.eseid.eid_idcard_svr.idcard";
    // ---------------------------------------------------------------------------------------------
    // 发送，静态函数，直接调用函数发送即可
    public static void sendLog(int level, String log) {
        Intent intent = new Intent(ACTION_LOG);
        intent.putExtra("level", level);
        intent.putExtra("log", log);
        context.sendBroadcast(intent);
    }
    // ---------------------------------------------------------------------------------------------
    // 接收：EidMsg 本身即为一个接收器
    public void init(Context context, UserCheckCardCB userCheckCardCB) {
        mUserCheckCardCB = userCheckCardCB;
        IntentFilter filter = new IntentFilter();
        filter.addAction(ACTION_LOG);
        context.registerReceiver(this, filter);
    }
    // 取消注册
    public void unregister(Context context) {
        context.unregisterReceiver(this);
    }
    // 消息接收
    @Override
    public void onReceive(Context context, Intent intent) {
        switch (intent.getAction()) {
            case ACTION_LOG:
                int level = intent.getIntExtra("level", 0);
                String log = intent.getStringExtra("log");
                mUserCheckCardCB.onLog(level, log);
                break;
        }
    }
}
```
