---
title: json
tags: 
    - json
categories: 
    - Android
description: json
date: 2022-08-25 10:25:59
updated: 2022-08-25 10:25:59
---

## JSONObject

```java
// String -> Json
String jsonStr = "{\"password\":\"123456\",\"username\":\"张三\"}";
JSONObject jsonObject = JSONObject.fromObject(jsonStr);
// Json -> String
System.out.println("java--->json \n " + jsonObject.toString());
// get
String username = jsonObject.getString("username");
// set
jsonObject.put("username", "宋发元");
jsonObject.put("age", 24);
```

## 
