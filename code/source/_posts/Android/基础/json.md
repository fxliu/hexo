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
// String -> Json: ["hard_version", "soft_version", "devid"]
JSONArray array = new JSONArray(params);
for(int i = 0; i < array.length(); i++) {
    Log.e(TAG, "getCardReaderInfo: " + array.getString(i));
}

// Json -> String
System.out.println("java--->json \n " + jsonObject.toString());
// get
String username = jsonObject.getString("username");
// set
jsonObject.put("username", "宋发元");
jsonObject.put("age", 24);
```

## JsonObject

```java
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import org.json.JSONObject;

public class JsonBuilder {
    JsonObject object;

    public JsonBuilder() {
        object = new JsonObject();
    }

    public JsonObject build() {
        return object;
    }

    // ---------------------------------------------------------------------------------------------
    public JsonBuilder put(String n, String v) {
        object.addProperty(n, v);
        return this;
    }

    public JsonBuilder put(String n, int v) {
        object.addProperty(n, v);
        return this;
    }

    public JsonBuilder put(String n, float v) {
        object.addProperty(n, v);
        return this;
    }

    public JsonBuilder put(String n, JsonObject v) {
        object.add(n, v);
        return this;
    }

    public JsonBuilder put(String n, JSONObject v) {
        put(n, JsonParser.parseString(v.toString()).getAsJsonObject());
        return this;
    }

    String getString(String key) {
        return object.get(key).getAsString();
    }

    int getInt(String key) {
        return object.get(key).getAsInt();
    }
}
```
