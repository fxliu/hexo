---
title: Application
tags: 
    - Application
categories: 
    - Android
description: Application
date: 2020-02-20 10:18:46
updated: 2020-02-20 10:18:46
---

## MyApplication

### 配置私有应用参数

```java
public class MyApplication extends Application {
    public static boolean test = true;
}
```

```xml
<application android:name=".MyApplication" />
```
