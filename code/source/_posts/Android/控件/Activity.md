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
<!--Standard-标准模式: 默认模式, 每次调用都启动一个新的activity-->
<activity android:name=".MainActivity" android:launchMode="standard" > ... </activity>
<!--singleTop-栈顶复用模式: 如果activity处于栈顶, 则直接使用, 否则创建新的-->
<activity android:name=".MainActivity" android:launchMode="singleTop"> ... </activity>
<!--singleTask-栈内复用模式-->
<activity android:name=".MainActivity" android:launchMode="singleTask" > ... </activity>
<!--singleInstance-全局唯一模式-->
<activity android:name=".MainActivity" android:launchMode="singleInstance" > ... </activity>
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
