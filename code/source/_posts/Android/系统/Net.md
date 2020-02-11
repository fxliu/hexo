---
title: 网络
tags: 
  - 网络
categories: 
  - Android
description: 网络, NET, HTTP
date: 2020-02-11 15:38:28
updated: 2020-02-11 15:38:28
---

## 简单GET

```java
import org.apache.commons.io.IOUtils;
import java.net.URL;

String re = IOUtils.toString(new URL("https://www.baidu.com/"), StandardCharsets.UTF_8);
```
