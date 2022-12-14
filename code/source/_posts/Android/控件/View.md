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
    private final Paint mPaint = new Paint();
    private final TextPaint mTextPaint = new TextPaint();
    private final Path mPath = new Path();

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
        // Paint
        mPaint.setColor(Color.YELLOW);
        mPaint.setStyle(Paint.Style.STROKE);    // 实线, Paint.Style.FILL 实心
        mPaint.setStrokeWidth(4);
        mPaint.setStrokeCap(Paint.Cap.ROUND);
        mPaint.setStrokeJoin(Paint.Join.ROUND);
        // Path
        mPath.moveTo(0, 0);
        mPath.rLineTo(100, 100);
    }

    @Override
    protected void onLayout(boolean changed, int left, int top, int right, int bottom) {
        super.onLayout(changed, left, top, right, bottom);
    }

    // 重绘
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        canvas.drawPath(mPath, mPaint);
        canvas.drawText("hello world", 100, 100, mTextPaint);
    }
}
```

## 翻转

```java
// Layout翻转: 包含所有子内容
public class ReverseLayout extends RelativeLayout {
    public boolean isReverse = true;
    public ReverseLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
    @Override
    public void dispatchDraw(Canvas canvas) {
        if (isReverse)
            canvas.scale(-1, 1, getWidth() / 2, getHeight() / 2);
        super.dispatchDraw(canvas);
    }
}
// view翻转: 仅自己
import android.content.Context;  
import android.graphics.Canvas;  
import android.util.AttributeSet;  
import android.widget.TextView;  

public class ReverseTextView extends TextView {
    public ReverseTextView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public void onDraw(Canvas canvas) {
        canvas.scale(-1, 1, getWidth() / 2, getHeight() / 2);
        super.onDraw(canvas);
    }
}
// SurfaceView 翻转 
public class TestSurfaceView extends SurfaceView implements SurfaceHolder.Callback{
    SurfaceHolder surfaceHolder;

    public TestSurfaceView(Context context, AttributeSet attrs) {
        super(context, attrs);
        surfaceHolder = this.getHolder();
        surfaceHolder.addCallback(this);
    }

    @Override  
    public void surfaceCreated(SurfaceHolder holder) {
        Canvas canvas = surfaceHolder.lockCanvas();
        //绘制之前先对画布进行翻转
        canvas.scale(-1,1, getWidth()/2,getHeight()/2);

        //开始自己的内容的绘制
        Paint paint = new Paint();
        canvas.drawColor(Color.WHITE);
        paint.setColor(Color.BLACK);
        paint.setTextSize(50);
        canvas.drawText("这是对SurfaceView的翻转",50,250,paint);
        surfaceHolder.unlockCanvasAndPost(canvas);
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {}

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {}
}
```

