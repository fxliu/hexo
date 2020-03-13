---
title: Fragment
tags: 
    - Fragment
categories: 
    - Android
description: Fragment
date: 2020-03-10 11:30:30
updated: 2020-03-10 11:30:30
---

## 基础

```xml
<!-- 新建 Fragment(Blank): TestFragment.java(fragment_test.xml) -->
<!-- 默认：FrameLayout，可以右键改为 LinearLayout 等其他 Layout -->
<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".TestFragment">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:text="hello_blank_fragment" />

</FrameLayout>
```

```xml
<!-- 方式一 -->
<!-- 调整 activity.xml 增加 fragment 控件，根据提示选择 关联新建的 TestFragment 即可 -->
<!-- fragment 控件一定要有id属性，否则会崩溃 -->
<androidx.constraintlayout.widget.ConstraintLayout
    ...
    tools:context=".MainActivity">
    <fragment
        android:id="@+id/fragment_test"
        android:name="com.es.test.TestFragment"
        .../>
</androidx.constraintlayout.widget.ConstraintLayout>
```

```xml
<!-- 方式二：activity.xml 中增加 FrameLayout 控件，然后代码方式补充 Fragment对象 -->
<!-- Frame 默认透明，可以设置 background 盖住下层内容 -->
<androidx.constraintlayout.widget.ConstraintLayout
    ...
    tools:context=".MainActivity">
    <FrameLayout
        android:id="@+id/frameLayout"
        android:layout_width="match_parent"
        android:background="@color/colorPrimary"
        android:layout_height="match_parent">
    </FrameLayout>
</androidx.constraintlayout.widget.ConstraintLayout>
```

```java
// 挂在 TestFragment 到 FrameLayout
FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
transaction.replace(R.id.frameLayout, new TestFragment());
// transaction.add(R.id.frameLayout, new TestFragment());
transaction.commit();
```
