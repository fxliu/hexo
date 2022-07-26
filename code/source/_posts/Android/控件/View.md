---
title: View
tags: 
    - View
categories: 
    - Android
description: View
date: 2022-07-08 09:58:55
updated: 2022-07-08 09:58:55
---

## 自绘

```java
// 背景透明
getBackground().setAlpha(0);
```

```java
// TextPaint
private TextPaint mTextPaint;
private float mTextWidth;
private float mTextHeight;
// Create
mTextPaint = new TextPaint();
mTextPaint.setFlags(Paint.ANTI_ALIAS_FLAG);
mTextPaint.setTextAlign(Paint.Align.LEFT);
// 属性
mTextPaint.setTextSize(mExampleDimension);
mTextPaint.setColor(mExampleColor);
// 计算文字区域大小
mTextWidth = mTextPaint.measureText(mExampleString);
Paint.FontMetrics fontMetrics = mTextPaint.getFontMetrics();
mTextHeight = fontMetrics.bottom;
```

```java
@Override
protected void onLayout(boolean changed, int left, int top, int right, int bottom) {
    super.onLayout(changed, left, top, right, bottom);
}
```
