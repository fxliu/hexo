---
title: FrameLayout
tags: 
    - FrameLayout
categories: 
    - Android
description: FrameLayout
date: 2022-07-29 22:15:37
updated: 2022-07-29 22:15:37
---

## 自定义 FrameLayout 组合控件

```xml
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="test" />
</FrameLayout>
```

```java
// 右键 -> New -> UiComponent -> Custom View
public class EsFaceFrame extends FrameLayout {
    FrameEsFaceBinding binding; // binding 支持

    // ---------------------------------------------------------------------------------------------
    public EsFaceFrame(Context context) {
        super(context);
        init(context);
    }

    public EsFaceFrame(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }

    public EsFaceFrame(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        init(context);
    }

    private void init(Context context) {
        // 绑定到 xml 资源
        // View view = View.inflate(context, R.layout.frame_es_face, this);
        binding = FrameEsFaceBinding.inflate(LayoutInflater.from(context), this, true);
    }
}
```
