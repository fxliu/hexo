---
title: Activity
tags: 
    - Activity
categories: 
    - Android
description: Activity
date: 2020-02-07 22:12:34
updated: 2020-02-07 22:12:34
---

## 基础

### java关联xml

```java
// MainActivity.java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    // 绑定：res/layout/activity_main.xml
    setContentView(R.layout.activity_main);
    // ...
}
```

### 属性

```xml
<activity
    android:noHistory="true"
    android:excludeFromRecents="true">
    无历史 + 不再显示到任务列表
</activity>
```

```xml
<!--Standard-标准模式: 默认模式, 每次调用都启动一个新的activity-->
<activity android:name=".MainActivity" android:launchMode="standard" > ... </activity>
<!--singleTop-栈顶复用模式: 如果activity处于栈顶, 则直接使用, 否则创建新的-->
<activity android:name=".MainActivity" android:launchMode="singleTop"> ... </activity>
<!--singleTask-栈内复用模式-->
<activity android:name=".MainActivity" android:launchMode="singleTask" > ... </activity>
<!--singleInstance-全局唯一模式-->
<activity android:name=".MainActivity" android:launchMode="singleInstance" > ... </activity>
```

```xml
<!-- 背景图：activity_main.xml -->
<androidx.constraintlayout.widget.ConstraintLayout
    android:background="@drawable/复制main_background"
    tools:context=".MainActivity">
</androidx.constraintlayout.widget.ConstraintLayout>
<!-- 复制文件“main_background.png”到“res/drawable”下即可-->
```

```xml
<!-- 基础 Layout -->
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    tools:context=".MainActivity">

</LinearLayout>
```

```xml
<!-- 强制竖屏 -->
<manifest>
    <application>
        <activity
            android:name=".MainActivity"
            android:screenOrientation="portrait"
            tools:ignore="LockedOrientationActivity">
        </activity>
    </application>
</manifest>
```

### 生命周期

```java
// 完整生存期
onCreate();     // 启动
onDestroy();    // 销毁
// 可见生存期
onStart();      // 对用户可见
onStop();       // 对用户不可见
// 前台生存期
onPause();      // 暂停, 离开前台
onResume()      // 继续, 进入前台
// 其他
onRestart()     // 停止(onStop)->运行(onStart), 该函数在onStart之前调用
onBackPressed() // 回退键处理, 可以当做用户强制退出
```

```java
// 终止生命周期
Activity.finish();      // 将最上面的Activity移出栈, 占用资源并不即时释放. 系统会在必要时调用onDestroy()完全销毁.
Activity.onDestory()    // 系统销毁这个Activity的实例在内存中占据的空间. onDestory是activity生命周期的最后一步.
System.exit(0)          // 退出整个应用程序
```

### 通讯

```java
// 调用Activity
void start() {
    // 当前Activity.this, 目标Activity.class
    Intent intent = new Intent(MainActivity.this, CheatActivity.class);
    intent.putExtra(key, value);
    // 无回调方式调用
    startActivity(intent);
    // 该函数非阻塞: 标记返回值标识
    startActivityForResult(intent, REQUEST_CODE_CHEAT);
}
// 接收Activity
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    String value = getIntent().getStringExtra(key);
    // 设置返回值
    Intent result = new Intent(this, ThisActivity.class);
    result.putExtra(key, value);
    setResult(RESULT_OK, result);
}
// 调用方Activity接收返回值
@Override
protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
    super.onActivityResult(requestCode, resultCode, intent);
    // REQUEST_CODE_CHEAT 对应startActivityForResult 第二个参数
    if(REQUEST_CODE_CHEAT == requestCode) {
        if(resultCode == Activity.RESULT_OK)
            Sting value = intent.getStringExtra(key));
    }
}
```

```java
// 回调封装
public class ResultFragment extends Fragment {
    public interface IListener {
        void onActivityResult(int requestCode, int resultCode, Intent intent);
    }

    private static final String TAG = ResultFragment.class.getSimpleName();
    private static final int mRequestCode = 1;
    private FragmentManager mFragmentManager;
    private IListener mListener;

    private ResultFragment(IListener listener) {
        mListener = listener;
    }

    private void create(FragmentActivity activity) {
        mFragmentManager = activity.getSupportFragmentManager();
        mFragmentManager
                .beginTransaction()
                .add(this, "")
                .commitAllowingStateLoss();
        mFragmentManager.executePendingTransactions();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        super.onActivityResult(requestCode, resultCode, intent);
        if (null != mListener) {
            mListener.onActivityResult(requestCode, resultCode, intent);
        }
        Log.i(TAG, String.format("requestCode: %d, resultCode: %d", requestCode, resultCode));
        // 回调之后自动释放
        mFragmentManager.beginTransaction()
                .remove(this).commit();
        onDestroy();
    }

    public static void startActivityForResult(FragmentActivity activity, Intent intent, IListener listener) {
        ResultFragment resultFragment = new ResultFragment(listener);
        resultFragment.create(activity);
        resultFragment.startActivityForResult(intent, mRequestCode);
    }
}
// 使用：TestActivity未设置返回值时会使用默认值，onActivityResult一定会触发
Intent intent = new Intent(app, TestActivity.class);
ResultFragment.startActivityForResult(app, intent, new ResultFragment.IListener() {
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if(resultCode == Activity.RESULT_OK) {
            String content = intent.getStringExtra("v");
            cbf.onCallBack(JsBridge.getSuccessObj(content).toString());
        } else {
            cbf.onCallBack(JsBridge.getError(-1, "cancel").toString());
        }
    }
});
```

### 翻转

```java
+ activity: 屏幕翻转会完全销毁activity,并重建
+ layout: 系统自动匹配最佳layout并加载, 默认加载layout, 横屏自动加载layout-land
```

```java
// 禁止横版
1. onCreate()中增加:
setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

2，Manifest.xml文件中为所有Activity加上配置属性android:screenOrientation="portrait"
```

```java
// activity 回收前数据存储
private static final String KEY_INDEX = "index";
private int mCurrentIndex = 0;
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    if(savedInstanceState != null)  # 首次启动为空
        mCurrentIndex = savedInstanceState.getInt(KEY_INDEX);
    ...
}
@Override
protected void onSaveInstanceState(Bundle outState) {
    super.onSaveInstanceState(outState);
    outState.putInt(KEY_INDEX, mCurrentIndex);
}
```

## 手动创建控件

```java
// xml中指定id，最外层Layout也可以指定id
LinearLayout linearLayout = this.findViewById(R.id.layoutNFC);
// 创建TextView，并指定控件参数
TextView tv = new TextView(this);
LinearLayout.LayoutParams layoutParams =   new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
tv.setLayoutParams(new LinearLayout.LayoutParams(layoutParams));
tv.setText("test");
// TextView添加到linearLayout
linearLayout.addView(tv);
```
