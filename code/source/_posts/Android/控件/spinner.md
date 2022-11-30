---
title: spinner
tags: 
    - spinner
categories: 
    - Android
description: View
date: 2022-11-30 16:53:49
updated: 2022-11-30 16:53:49
---
## 基础使用

```xml
<!-- layout:my_spinner.xml -->
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@android:id/text1"
    style="?android:attr/spinnerItemStyle"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:textSize="36sp"
    android:ellipsize="marquee"
    android:gravity="center_vertical"
    android:singleLine="true"
    android:padding="10sp"
    android:textAlignment="inherit" />
```

```xml
<!--activity.xml-->
<Spinner
    android:id="@+id/spinner"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content" />
```

```java
String[] items;
// items 添加数据
Spinner spinner = findViewById(R.id.spinner);
SpinnerAdapter adapter = new ArrayAdapter<>(this, R.layout.my_spinner, items);
spinner.setAdapter(adapter);
```
