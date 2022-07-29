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
public class EsFaceRectView extends View {
    private final TextPaint mTextPaint = new TextPaint();

    public EsFaceRectView(Context context) {
        super(context);
        init();
    }

    public EsFaceRectView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public EsFaceRectView(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        init();
    }

    private void init() {
        // TextPaint
        mTextPaint.setTextSize(27);
        mTextPaint.setFlags(Paint.ANTI_ALIAS_FLAG);
        mTextPaint.setTextAlign(Paint.Align.LEFT);
        mTextPaint.setColor(Color.YELLOW);
    }

    @Override
    protected void onLayout(boolean changed, int left, int top, int right, int bottom) {
        super.onLayout(changed, left, top, right, bottom);
    }

    // 重绘
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        canvas.drawText("hello world", 100, 100, mTextPaint);
    }
}
```
