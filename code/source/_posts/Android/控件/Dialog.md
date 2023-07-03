---
title: Dialog
tags: 
    - Dialog
categories: 
    - Android
description: Dialog
date: 2023-06-30 14:43:34
updated: 2023-06-30 14:43:34
---

## AlertDialog

```java
// 普通对话框
// .setNeutralButton("第三个按钮",listener)
AlertDialog dialog = new AlertDialog.Builder(this)
              .setIcon(R.mipmap.icon)//设置标题的图片
              .setTitle("我是对话框")//设置对话框的标题
              .setMessage("我是对话框的内容")//设置对话框的内容
              //设置对话框的按钮
              .setNegativeButton("取消", new DialogInterface.OnClickListener() {
                  @Override
                  public void onClick(DialogInterface dialog, int which) {
                      Toast.makeText(MainActivity.this, "点击了取消按钮", Toast.LENGTH_SHORT).show();
                      dialog.dismiss();
                  }
              })
              .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                  @Override
                  public void onClick(DialogInterface dialog, int which) {
                      Toast.makeText(MainActivity.this, "点击了确定的按钮", Toast.LENGTH_SHORT).show();
                      dialog.dismiss();
                  }
              }).create();
      dialog.show();
```

```java
final String items[] = {"我是Item一", "我是Item二", "我是Item三", "我是Item四"};
AlertDialog dialog = new AlertDialog.Builder(this)
        .setIcon(R.mipmap.icon)//设置标题的图片
        .setTitle("列表对话框")//设置对话框的标题
        .setItems(items, new DialogInterface.OnClickListener() {    // 支持适配器模式: setAdapter
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Toast.makeText(MainActivity.this, items[which], Toast.LENGTH_SHORT).show();
            }
        })
        .setNegativeButton("取消", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        })
        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        }).create();
dialog.show();
```

```java
// 单选列表对话框
 final String items[] = {"我是Item一", "我是Item二", "我是Item三", "我是Item四"};
AlertDialog dialog = new AlertDialog.Builder(this)
        .setIcon(R.mipmap.icon)//设置标题的图片
        .setTitle("单选列表对话框")//设置对话框的标题
        .setSingleChoiceItems(items, 1, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Toast.makeText(MainActivity.this, items[which], Toast.LENGTH_SHORT).show();
            }
        })
        .setNegativeButton("取消", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        })
        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        }).create();
dialog.show();
```

```java
// 多选对话框
final String items[] = {"我是Item一", "我是Item二", "我是Item三", "我是Item四"};
final boolean checkedItems[] = {true, false, true, false};
AlertDialog dialog = new AlertDialog.Builder(this)
        .setIcon(R.mipmap.icon)//设置标题的图片
        .setTitle("多选对话框")//设置对话框的标题
        .setMultiChoiceItems(items, checkedItems, new DialogInterface.OnMultiChoiceClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which, boolean isChecked) {
                checkedItems[which] = isChecked;
            }
        })
        .setNegativeButton("取消", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        })
        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                for (int i = 0; i < checkedItems.length; i++) {
                    if (checkedItems[i]) {
                        Toast.makeText(MainActivity.this, "选中了" + i, Toast.LENGTH_SHORT).show();
                    }
                }
                dialog.dismiss();
            }
        }).create();
dialog.show();
```

```java
// 自定义输入框
// View view = getLayoutInflater().inflate(R.layout.half_dialog_view, null);
// final EditText editText = (EditText) view.findViewById(R.id.dialog_edit);
final EditText editText = new EditText(this);
AlertDialog dialog = new AlertDialog.Builder(this)
        .setIcon(R.mipmap.icon)//设置标题的图片
        .setTitle("半自定义对话框")//设置对话框的标题
        .setView(view)            //  这里的view可以是任意自定义view
        .setNegativeButton("取消", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        })
        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String content = editText.getText().toString();
                Toast.makeText(MainActivity.this, content, Toast.LENGTH_SHORT).show();
                dialog.dismiss();
            }
        }).create();
dialog.show();
```

```java
// 进度条对话框
 ProgressDialog dialog = new ProgressDialog(this);
dialog.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);   // 指定样式
dialog.setMessage("正在加载中");
dialog.setMax(100);

final Timer timer = new Timer();
timer.schedule(new TimerTask() {
    int progress = 0;
    @Override
    public void run() {
        dialog.setProgress(progress += 5);
        if (progress == 100) {
            timer.cancel();
        }
    }
}, 0, 1000);
dialog.show();
```

## 自定义对话框

* 自定义Dialog的style
```xml
	 <!--对话框的样式-->
    <style name="NormalDialogStyle">
	    <!--对话框背景 -->
        <item name="android:windowBackground">@android:color/transparent</item>
        <!--边框 -->
        <item name="android:windowFrame">@null</item>
        <!--没有标题 -->
        <item name="android:windowNoTitle">true</item>
        <!-- 是否浮现在Activity之上 -->
        <item name="android:windowIsFloating">true</item>
        <!--背景透明 -->
        <item name="android:windowIsTranslucent">false</item>
        <!-- 是否有覆盖 -->
        <item name="android:windowContentOverlay">@null</item>
        <!--进出的显示动画 -->
        <item name="android:windowAnimationStyle">@style/normalDialogAnim</item>
        <!--背景变暗-->
        <item name="android:backgroundDimEnabled">true</item>
    </style>
    <!--对话框动画-->
    <style name="normalDialogAnim" parent="android:Animation">
        <item name="@android:windowEnterAnimation">@anim/normal_dialog_enter</item>
        <item name="@android:windowExitAnimation">@anim/normal_dialog_exit</item>
    </style>
```
* Dialog
```java
/**
 * 自定义对话框
 */
private void customDialog() {
    final Dialog dialog = new Dialog(this, R.style.NormalDialogStyle);
    View view = View.inflate(this, R.layout.dialog_normal, null);
    TextView cancel = (TextView) view.findViewById(R.id.cancel);
    TextView confirm = (TextView) view.findViewById(R.id.confirm);
    dialog.setContentView(view);
    //使得点击对话框外部不消失对话框
    dialog.setCanceledOnTouchOutside(true);
    //设置对话框的大小
    view.setMinimumHeight((int) (ScreenSizeUtils.getInstance(this).getScreenHeight() * 0.23f));
    Window dialogWindow = dialog.getWindow();
    WindowManager.LayoutParams lp = dialogWindow.getAttributes();
    lp.width = (int) (ScreenSizeUtils.getInstance(this).getScreenWidth() * 0.75f);
    lp.height = WindowManager.LayoutParams.WRAP_CONTENT;
    lp.gravity = Gravity.CENTER;
    dialogWindow.setAttributes(lp);
    cancel.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            dialog.dismiss();
        }
    });
    confirm.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            dialog.dismiss();
        }
    });
    dialog.show();
}
public class ScreenSizeUtils {
    private static ScreenSizeUtils instance = null;
    private int screenWidth, screenHeight;
    public static ScreenSizeUtils getInstance(Context mContext) {
        if (instance == null) {
            synchronized (ScreenSizeUtils.class) {
                if (instance == null)
                    instance = new ScreenSizeUtils(mContext);
            }
        }
        return instance;
    }
    private ScreenSizeUtils(Context mContext) {
        WindowManager manager = (WindowManager) mContext.getSystemService(Context.WINDOW_SERVICE);
        DisplayMetrics dm = new DisplayMetrics();
        manager.getDefaultDisplay().getMetrics(dm);
        screenWidth = dm.widthPixels;// 获取屏幕分辨率宽度
        screenHeight = dm.heightPixels;// 获取屏幕分辨率高度
    }
    //获取屏幕宽度
    public int getScreenWidth() {
        return screenWidth;
    }
    //获取屏幕高度
    public int getScreenHeight() {
        return screenHeight;
    }
}
```

## 底部对话框

```xml
<!-- dialog_bottom.xml -->
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@android:color/transparent"
    android:orientation="vertical">

    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@drawable/round_corner"
        android:text="拍照" />

    <TextView
        android:layout_width="match_parent"
        android:layout_height="1dp"
        android:layout_marginLeft="10dp"
        android:layout_marginRight="10dp"
        android:background="#ddd" />

    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@drawable/round_corner"
        android:text="相册" />

    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="10dp"
        android:background="@drawable/round_corner"
        android:text="取消" />

    <View
        android:layout_width="match_parent"
        android:layout_height="15dp" />
</LinearLayout>
```

```java
// 布局
Dialog dialog = new Dialog(this, R.style.NormalDialogStyle);
View view = View.inflate(this, R.layout.dialog_bottom, null);
dialog.setContentView(view);
dialog.setCanceledOnTouchOutside(true);
view.setMinimumHeight((int) (ScreenSizeUtils.getInstance(this).getScreenHeight() * 0.23f));
Window dialogWindow = dialog.getWindow();
WindowManager.LayoutParams lp = dialogWindow.getAttributes();
lp.width = (int) (ScreenSizeUtils.getInstance(this).getScreenWidth() * 0.9f);
lp.height = WindowManager.LayoutParams.WRAP_CONTENT;
lp.gravity = Gravity.BOTTOM;
dialogWindow.setAttributes(lp);
dialog.show();
```


