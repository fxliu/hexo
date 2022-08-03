---
title: aidl
tags: 
    - aidl
categories: 
    - Android
description: aidl
date: 2022-08-03 21:00:08
updated: 2022-08-03 21:00:08
---

## 基础应用

```java
// IImoocAIDL.aidl
// 点击同步按钮（一定要先同步），查看是否生成IImoocAIDL文件
interface IImoocAIDL {    
    int add(int num1,int num2);
}
```

```xml
<!-- 服务端: 注册 --> 
<service android:name=".IRemoteService"
    android:process=":remote"
    android:exported="true">
    <intent-filter>
        <action android:name="com.***.IRomoteService"/>
    </intent-filter>
</service>
```

```java
// 服务端：实现 IImoocAIDL
public class IRemoteService extends Service {
    //客户端绑定service时会执行
    @Override
    public IBinder onBind(Intent intent) {
        return iBinder;
    }
    private IBinder iBinder = new IImoocAIDL.Stub(){
        @Override
        public int add(int num1, int num2) throws RemoteException {
            Log.e("TAG","收到了来自客户端的请求" + num1 + "+" + num2 );
            return num1 + num2;
        }
    };
}

```

```java
// 客户端：bind回调参数
private IImoocAIDL iImoocAIDL;
private ServiceConnection conn = new ServiceConnection() {

    //绑定服务，回调onBind()方法
    @Override
    public void onServiceConnected(ComponentName name, IBinder service) {
        iImoocAIDL = IImoocAIDL.Stub.asInterface(service);
    }

    @Override
    public void onServiceDisconnected(ComponentName name) {
        iImoocAIDL = null;
    }
};
// 绑定 - 新版本（5.0后）必须显式intent启动 绑定服务
Intent intent = new Intent();
intent.setAction("com.***.IRomoteService");
intent.setComponent(new ComponentName("com.***","com.***.IRemoteService"));
//绑定的时候服务端自动创建
bindService(intent,conn, Context.BIND_AUTO_CREATE);

// AIDL使用
iImoocAIDL.add(1,2);
```
