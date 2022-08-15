---
title: Tools
tags: 
    - Tools
categories: 
    - Android
description: Tools
date: 2022-08-15 11:47:07
updated: 2022-08-15 11:47:07
---

## 常用小工具

## 
```java
public class Tools {
    static public void sleep(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException ignored) {
        }
    }
}
```

