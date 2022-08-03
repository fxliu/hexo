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

## Service

* 服务不能自己运行，需要通过调用Context.startService()或Context.bindService()方法启动服务。这两个方法都可以启动Service，但是它们的使用场合有所不同。
* startService()方法启用服务，调用者与服务之间没有关连，即使调用者退出了，服务仍然运行。
* startService()方法启动服务，在服务未被创建时，系统会先调用服务的onCreate()方法，接着调用onStart()方法。
* startService()方法多次调用并不会导致多次创建服务，但会导致多次调用onStart()方法。
* startService()方法启动的服务，只能调用Context.stopService()方法结束服务，服务结束时会调用onDestroy()方法。

* bindService()方法启用服务，调用者与服务绑定在了一起，调用者一旦退出，服务也就终止，大有“不求同时生，必须同时死”的特点。 
* bindService()方法启动服务，在服务未被创建时，系统会先调用服务的onCreate()方法，接着调用onBind()方法。
* 调用者和服务绑定在一起，调用者退出了，系统就会先调用服务的onUnbind()方法，接着调用onDestroy()方法。
* bindService()方法前服务已经被绑定，多次调用bindService()方法并不会导致多次创建服务及绑定(也就是说onCreate()和onBind()方法并不会被多次调用)。
* 如果调用者希望与正在绑定的服务解除绑定，可以调用unbindService()方法，调用该方法也会导致系统调用服务的onUnbind()-->onDestroy()方法。

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

## 应用

```java
// 服务启动
public final class SvrManager {
    @SuppressLint("StaticFieldLeak")
    private static Context sApp;

    private static final Map<Class<? extends Service>, IBinder> svrBind = new HashMap<>();

    public static void initialize(@NonNull Context app) {
        sApp = app;
    }

    public static boolean IsSvrRunning(Context context, String svrName) {
        ActivityManager am = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
        List<ActivityManager.RunningServiceInfo> infos = am.getRunningServices(1000);

        for (ActivityManager.RunningServiceInfo info : infos) {
            if (info.service.getClassName().equals(svrName)) {
                return true;
            }
        }
        return false;
    }

    public static void startServiceSafely(Context context, Class<?> cls) {
        if (!IsSvrRunning(context, cls.getName())) {
            Intent eidIntent = new Intent(context, cls);
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                context.startForegroundService(eidIntent);
            else
                context.startService(eidIntent);
        }
    }

    public static void restartEidService(Context context) {
        Intent eidIntent = new Intent(context, EidIDCardService.class);
        eidIntent.setAction(EidIDCardService.ACTION_RESTART);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
            context.startForegroundService(eidIntent);
        else
            context.startService(eidIntent);
    }

    public static void startServiceMayBind(@NonNull final Class<? extends Service> serviceClass) {
        startServiceSafely(sApp, serviceClass);
        if (svrBind.get(serviceClass) == null) {
            final Intent intent = new Intent(sApp, serviceClass);
            ServiceConnection connection = new ServiceConnection() {
                @Override
                public void onServiceConnected(ComponentName name, IBinder service) {
                    svrBind.put(serviceClass, service);
                }

                @Override
                public void onServiceDisconnected(ComponentName name) {
                    svrBind.remove(serviceClass);
                    startServiceSafely(sApp, serviceClass);
                    sApp.bindService(intent, this, Context.BIND_AUTO_CREATE);
                }
            };
            sApp.getApplicationContext().bindService(intent, connection, Context.BIND_AUTO_CREATE);
        }
    }

    static IBinder getBind(@NonNull final Class<? extends Service> serviceClass) {
        return svrBind.get(serviceClass);
    }
}

```

```java
// 服务
public final class EidIDCardService extends Service {
    private static final String ID = "eid_channel";
    private static final String NAME = "eid";
    public static final String ACTION_RESTART = "com.eseid.eid_idcard_svr";
    private boolean restart = false;
    private UsbMonitor usbMonitor;
    // 双服务监控
    private static final Thread watchThread = new Thread(new Runnable() {
        @Override
        public void run() {
            while (true) {
                try {
                    XLog.d("EidIDCardService: Watch Working");
                    for (int i = 0; i < 60; i++) {
                        SvrManager.startServiceMayBind(WatchDogService.class);
                        Thread.sleep(1000);
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    });

    // SDK多线程
    final EidIDCard eidIDCard = new EidIDCard();
    private final Thread eidIDCardThread = new Thread(new Runnable() {
        @Override
        public void run() {
            while (true) {
                try {
                    XLog.d("EidIDCardService: Working");
                    for (int i = 0; i < 60; i++) {
                        if (restart) {
                            eidIDCard.stop();
                            restart = false;
                        }
                        eidIDCard.run(getApplicationContext());
                        Thread.sleep(1000);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    });

    public EidIDCardService() {
    }

    private synchronized void start() {
        if (watchThread.isAlive() && eidIDCardThread.isAlive()) {
            EidMsg.sendLogD("EidIDCardService: isAlive");
            return;
        }
        EidMsg.sendLogI("EidIDCardService: start");
        if (usbMonitor == null) {
            usbMonitor = new UsbMonitor(getApplicationContext());
            usbMonitor.monitor(usbMonitorCB);
        }

        if (Build.VERSION.SDK_INT >= 26)
            setForeground(getApplicationContext());

        if (!EsProperties.init(getApplicationContext()))
            XLog.e("EsProperties.init Error");

        if (!watchThread.isAlive()) {
            XLog.d("watchThread Start");
            watchThread.start();
        }
        if (!eidIDCardThread.isAlive()) {
            XLog.d("eidIDCardThread Start");
            eidIDCardThread.start();
        }

        //守护 Service 组件的启用状态, 使其不被禁用
        getPackageManager().setComponentEnabledSetting(
                new ComponentName(getPackageName(), EidIDCardService.class.getName()),
                PackageManager.COMPONENT_ENABLED_STATE_ENABLED, PackageManager.DONT_KILL_APP);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        EidMsg.init(getApplicationContext());
        XLog.d("EidIDCardService: onCreate");
        if(Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
            Context context = getApplicationContext();
            NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            Intent intent = new Intent(context, MainActivity.class);
            PendingIntent pendingIntent = PendingIntent.getBroadcast(context, 0, intent, 0);

            Notification notification = new NotificationCompat.Builder(context, "default")
                    .setContentTitle("读证服务")
                    .setContentText("读证服务运行中...")
                    .setSmallIcon(R.mipmap.ic_launcher_notification)
//                .setAutoCancel(true) // 打开程序后图标消失
                    .setOngoing(true)
                    .setContentIntent(pendingIntent)
                    .build();
//            manager.notify(1, notification);
            startForeground(1, notification);
        }
        start();
    }

    @Override
    public IBinder onBind(Intent intent) {
        XLog.d("EidIDCardService: onBind");
        start();
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if(intent != null) {
            String strAction = intent.getAction();
            if (strAction != null && strAction.equals(ACTION_RESTART)) {
                restart = true;
                XLog.d("EidIDCardService: ACTION_RESTART");
            }
        }
        start();
        return START_STICKY;    // 被kill掉后自动重启
        // return super.onStartCommand(intent, flags, startId);
    }

    public void onDestroy() {
        EidMsg.sendLogW("EidIDCardService: onDestroy");
        XLog.w("EidIDCardService: onDestroy");
        super.onDestroy();
    }

    @TargetApi(26)
    private void setForeground(Context context) {
        NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        NotificationChannel channel = new NotificationChannel(ID, NAME, NotificationManager.IMPORTANCE_HIGH);
        manager.createNotificationChannel(channel);

        Intent intent = new Intent(context, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(context, 0, intent, 0);

        Notification notification = new Notification.Builder(this, ID)
                .setContentTitle("读证服务")
                .setContentText("读证服务运行中...")
                .setSmallIcon(R.mipmap.ic_launcher_notification)
//                .setAutoCancel(true) // 打开程序后图标消失
                .setOngoing(true)
                .setContentIntent(pendingIntent)
                .build();
        startForeground(1, notification);
    }

    // ---------------------------------------------------------------------------------------------
    // USB监控
    private final static int hidVendorId = 0x0483;
    private final static int hidProductId = 0xE806;
    private final UsbMonitor.MonitorCB usbMonitorCB = new UsbMonitor.MonitorCB() {
        boolean isMonitor(UsbDevice usbDevice, int devModeIdx) {
            int vid = 0, pid = 0;
            if (EidStruct.isUsbHid(devModeIdx)) {
                vid = hidVendorId;
                pid = hidProductId;
            }
            return (usbDevice.getProductId() == pid && usbDevice.getVendorId() == vid);
        }

        @Override
        public void attached(UsbDevice usbDevice) {
            int devModeIdx = EidStruct.getDevModeIdx(EsProperties.getDevMode());
            if (!isMonitor(usbDevice, devModeIdx))
                return;
            if (usbDevice.getProductId() == hidProductId) {
                XLog.w("USBHID 设备上线");
            }
            // 禁用root模式, 提高兼容性
            // RootCmd.execRootCmdSilent("chmod -R 777 /dev/bus/usb");
            restart = true;
        }

        @Override
        public void detached(UsbDevice usbDevice) {
            int devModeIdx = EidStruct.getDevModeIdx(EsProperties.getDevMode());
            if (!isMonitor(usbDevice, devModeIdx))
                return;
            if (usbDevice.getProductId() == hidProductId) {
                XLog.w("USBHID 设备掉线");
            }
            XLog.e("USBHID 设备掉线");
            restart = true;
        }
    };
}
```

```java
// 双服务监控 包活机制
public class WatchDogService extends Service {
    private static final String ID = "eid_watch_channel";
    private static final String NAME = "eid_watch";

    // job多线程，定时检查 EidIDCardService 是否存在
    private static final Thread watchThread = new Thread(new Runnable() {
        @Override
        public void run() {
            while (true) {
                try {
                    XLog.d("WatchDogService: Watch Working");
                    for (int i = 0; i < 60; i++) {
                        SvrManager.startServiceMayBind(EidIDCardService.class);
                        Thread.sleep(1000);
                    }
                } catch (Exception e) {
                    XLog.d(e);
                }
            }
        }
    });

    public WatchDogService() {
    }

    private void start() {
        if (watchThread.isAlive()) {
            return;
        }
        EidMsg.sendLogD("WatchDogService: start");

        if (Build.VERSION.SDK_INT >= 26)
            setForeground(getApplicationContext());

        XLog.d("watchThread Start");
        watchThread.start();

        //守护 Service 组件的启用状态, 使其不被禁用
        getPackageManager().setComponentEnabledSetting(
                new ComponentName(getPackageName(), WatchDogService.class.getName()),
                PackageManager.COMPONENT_ENABLED_STATE_ENABLED, PackageManager.DONT_KILL_APP);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        EidMsg.init(getApplicationContext());
        XLog.d("WatchDogService: onCreate");
        start();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        XLog.d("WatchDogService: onBind");
        start();
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        XLog.d("WatchDogService: onStartCommand");
        start();
        return START_STICKY;    // 被kill掉后自动重启
        // return super.onStartCommand(intent, flags, startId);
    }

    public void onDestroy() {
        EidMsg.sendLogW("WatchDogService: start");
        XLog.w("WatchDogService: onDestroy");
        super.onDestroy();
    }

    @TargetApi(26)
    private void setForeground(Context context) {
        NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        NotificationChannel channel = new NotificationChannel(ID, NAME, NotificationManager.IMPORTANCE_HIGH);
        manager.createNotificationChannel(channel);

        Intent intent = new Intent(context, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(context, 0, intent, 0);

        Notification notification = new Notification.Builder(this, ID)
                .setContentTitle("EID")
                .setContentText("EID监控服务运行中...")
                .setSmallIcon(R.mipmap.ic_launcher)
//                .setAutoCancel(true) // 打开程序后图标消失
                .setOngoing(true)
                .setContentIntent(pendingIntent)
                .build();
        startForeground(1, notification);
    }
}
```
