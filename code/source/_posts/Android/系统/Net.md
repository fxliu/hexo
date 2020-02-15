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

### 无法访问HTTP问题

```xml
<!--AndroidManifest.xml
补充 android:networkSecurityConfig
-->
<application
        android:networkSecurityConfig="@xml/network_security_config">
</application>

<!--network_security_config.xml-->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true" />
</network-security-config>
```

## android-async-http / httpclient

```java
import cz.msebera.android.httpclient.Header;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

void test() {
    // http post
    RequestParams requestParams = new RequestParams();
    requestParams.put("username", "abc");
    requestParams.put("password", "123");

    AsyncHttpClient client = new AsyncHttpClient();
    client.post("https://*/test.php", requestParams, new AsyncHttpResponseHandler() {
        @Override
        public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
            Log.d(TAG, new String(responseBody));
        }
        @Override
        public void onFailure(int statusCode, Header[] headers, byte[] responseBytes, Throwable throwable) {
            Log.d(TAG, "onFailure");
        }
        public void onFinish() {
            super.onFinish();
            Log.d(TAG, "onFinish");
        }
    });
}
// get
RequestParams requestParams = new RequestParams();
    requestParams.put("username", "abc");
    requestParams.put("password", "123");
    client.get(url, requestParams, jsonHttpResponseHandler );
```

```java
// 请求参数定义1：
RequestParams params=new RequestParams("single","value");
// 请求参数定义2：
HashMap<String,String> paramMap=new HashMap<String,String>();
paramMap.put("key","value");
RequestParams params=new RequestParams(paramMap);
```

### android-async-http / 上传文件

```java
// 文件流
InputStream myInputStream = new ByteArrayInputStream("asdf".getBytes());
RequestParams params=new RequestParams();
params.put("secret_passwords", myInputStream, "password.txt");
params.put("secret_passwords", myInputStream, "test.jpg", "image/jpeg");

// 文件对象
RequestParams params=new RequestParams();
try {
    params.put("timg.jpg", new File(path));
    params.put("timg.jpg", new File(path), "image/jpeg");
} catch (FileNotFoundException e) {
    e.printStackTrace();
}
```

```java
// 文本数据
// JsonHttpResponseHandler, TextHttpResponseHandler
client.post("https://*/test.php", requestParams, new AsyncHttpResponseHandler() {
    @Override
    public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
    }
    @Override
    public void onFailure(int statusCode, Header[] headers, byte[] responseBytes, Throwable throwable) {
    }
});
// 文件下载
client.post("https://**", requestParams, new FileAsyncHttpResponseHandler(new File(path)) {
    @Override
    public void onSuccess(int statusCode, Header[] headers, File file) {
    }

    @Override
    public void onFailure(int statusCode, Header[] headers,Throwable throwable, File file) {
    }
});
```
