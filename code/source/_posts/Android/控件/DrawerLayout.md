---
title: 侧边栏
tags: 
    - DrawerLayout
categories: 
    - Android
description: DrawerLayout
date: 2023-05-10 16:19:57
updated: 2023-05-10 16:19:57
---

## 基础使用

```xml
<androidx.drawerlayout.widget.DrawerLayout
    android:id="@+id/drawer"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <!--主页面-->
    <androidx.constraintlayout.widget.ConstraintLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:background="@color/design_default_color_on_primary">

        <Button
            android:id="@+id/open"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="打开侧边栏"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toTopOf="parent" />

    </androidx.constraintlayout.widget.ConstraintLayout>
    <!--侧边栏: 根据不同的layout_gravity参数, 可以定义多个-->
    <!--
      注意配置clickable参数, 否则点击事件会穿透侧边栏
    -->
    <androidx.constraintlayout.widget.ConstraintLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_gravity="start"
        android:clickable="true"
        android:focusable="true"
        android:background="@color/design_default_color_primary">

        <Button
            android:id="@+id/close"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="100dp"
            android:text="关闭侧边栏"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toTopOf="parent" />

    </androidx.constraintlayout.widget.ConstraintLayout>

</androidx.drawerlayout.widget.DrawerLayout>
```

```java
// 基础应用
DrawerLayout drawerLayout = findViewById(R.id.drawer);
drawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED);
// 侧边栏事件监听
drawerLayout.addDrawerListener(new DrawerLayout.SimpleDrawerListener() {
    @Override
    public void onDrawerSlide(View drawerView, float slideOffset) {
        super.onDrawerSlide(drawerView, slideOffset);
    }
    @Override
    public void onDrawerOpened(View drawerView) {
        super.onDrawerOpened(drawerView);
        drawerView.setClickable(true);  // 解决点击穿透问题
    }
    @Override
    public void onDrawerClosed(View drawerView) {
        super.onDrawerClosed(drawerView);
    }
    @Override
    public void onDrawerStateChanged(int newState) {
        super.onDrawerStateChanged(newState);
    }
});
// 打开指定侧边栏
drawerLayout.openDrawer(GravityCompat.END);
// 开关拖动功能
drawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_UNLOCKED);
drawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED);
```
