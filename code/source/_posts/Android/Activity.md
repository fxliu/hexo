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

## 关联

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

## 手动创建控件

```java
// xml中指定id，最外层Layout也可以指定id
LinearLayout linearLayout = this.findViewById(R.id.layoutNFC);
// 创建TextView，并指定控件参数
TextView tv = new TextView(this);
LinearLayout.LayoutParams layoutParams =   new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
tv.setLayoutParams(new LinearLayout.LayoutParams(layoutParams));
tv.setText("asdf");
// TextView添加到linearLayout
linearLayout.addView(tv);
```
