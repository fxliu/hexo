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

```xml
<application>
    <!-- 联网权限 -->
    <uses-permission android:name="android.permission.INTERNET" />
</application>
```

```java
// implementation 'commons-io:commons-io:2.8.0'
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
    // 文本数据
    // JsonHttpResponseHandler, TextHttpResponseHandler
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

### android-async-http / 文件上传 / 文件下载

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

## okhttp

[官方文档](https://square.github.io/okhttp/)

`implementation "com.squareup.okhttp3:okhttp:4.10.0"`

### 简单使用

```java
// client builder
OkHttpClient.Builder builder = new OkHttpClient.Builder();
builder.connectTimeout(5 * 1000, TimeUnit.SECONDS)
        .readTimeout(5 * 1000, TimeUnit.SECONDS)
        .writeTimeout(5 * 1000, TimeUnit.SECONDS)
        .retryOnConnectionFailure(true);
// client
OkHttpClient client = builder.build();
// Post数据
FormBody requestBody = new FormBody.Builder()
        .add("username", "admin")
        .add("password", "admin")
        .build();
// Request
Request request = new Request.Builder()
        .url("https://t.dnndo.com/lfx_test.php")
        .post(requestBody)
        .build();
// 请求: 同步
Response response = mClient.newCall(request).execute();
response.body().string();
// 请求: 异步
client.newCall(request).enqueue(new Callback() {
    @Override
    public void onFailure(@NotNull Call call, @NotNull IOException e) {
        Log.e(TAG, Objects.requireNonNull(e.getMessage()));
    }

    @Override
    public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
        Headers responseHeaders = response.headers();
        for (int i = 0; i < responseHeaders.size(); i++) {
            Log.e(TAG, responseHeaders.name(i) + ": " + responseHeaders.value(i));
        }
        Log.e(TAG, Objects.requireNonNull(response.body()).string());
    }
});
```
```java
// Response response: 说明
response.body();    // body只能调用一次
```

### 拦截器

```java
mOkHttpClient = new OkHttpClient().newBuilder()
    .addInterceptor(new LoggerInterceptor())
// 拦截器：继承 Interceptor 接口即可
public class LoggerInterceptor implements Interceptor {

    @Override
    public Response intercept(@NonNull Chain chain) throws IOException {
        // 返回请求对象，也可以重定向（重新创建一个新的）
        return chain.request();
    }
}

```

### MediaType

+ text/html | text/plain | text/xml
+ image/gif | image/jpeg | image/png
+ application/xhtml+xml | application/xml | application/atom+xml
+ application/json | application/pdf | application/octet-stream

### Request

```java
// GET
public static Request getRequest(String url) {
    return new Request.Builder()
            .url(url)
            .get()      // 默认get
            .build();
}
public static Request myHeaderRequest(String url) {
    // 自定义头
    return new Request.Builder()
            .url(url)
            .header("User-Agent", "OkHttp Headers.java")
            .addHeader("Accept", "application/json; q=0.5")
            .addHeader("Accept", "application/vnd.github.v3+json")
            .build();
}
public static Request textRequest(String url) {
    // 自定义格式字符串
    final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    String body = "{}";
    return new Request.Builder()
            .url(url)
            .post(RequestBody.create(body, JSON))
            .build();
}
public static Request streamRequest(String url) {
    RequestBody requestBody = new RequestBody() {
        @Nullable
        @Override
        public MediaType contentType() {
            return MediaType.parse("application/json; charset=utf-8");
        }

        @Override
        public void writeTo(BufferedSink sink) throws IOException {
            sink.writeUtf8("{}");
        }
    };

    return new Request.Builder()
            .url(url)
            .post(requestBody)
            .build();
}
public static Request formRequest() {
    // 常规参数
    RequestBody requestBody = new FormBody.Builder()
            .add("search", "Jurassic Park")
            .build();
    // 文件
    File file = new File(Environment.getExternalStorageDirectory() + "test.txt");
    MediaType MEDIATYPE = MediaType.parse("text/plain; charset=utf-8");
    RequestBody requestBody = RequestBody.create(MEDIATYPE, file);
    // 表单
    File file = new File(Environment.getExternalStorageDirectory(), "zhuangqilu.png");
    RequestBody  requestBody = new MultipartBody.Builder()
        //设置类型是表单
        .setType(MultipartBody.FORM)
        //添加数据
        .addFormDataPart("username","zhangqilu")
        .addFormDataPart("age","25")
        .addFormDataPart("image", "zhangqilu.png", RequestBody.create(MediaType.parse("image/png"),file))
        .build();
    // 表单
    FormBody requestBody = new FormBody.Builder()
        .add("username", "admin")
        .add("password", "admin")
        .build();
    return new Request.Builder()
            .url("https://en.wikipedia.org/w/index.php")
            .post(requestBody)
            .build();
}
```

### 请求同步

```java
new Thread(new Runnable() {
    @Override
    public void run() {
        try {
            // 注意Android不允许主线程访问网络，execute方法必须在线程中执行
            Response response = client.newCall(request).execute();
            Log.e(TAG, Objects.requireNonNull(response.body()).string());
        } catch (IOException e) {
            Log.e(TAG, Objects.requireNonNull(e.getMessage()));
        }
    }
}).start();
```

## APP升级

+ [AutoUpdateProject](https://github.com/MZCretin/AutoUpdateProject)
+ [ApkUpdater](https://github.com/hss01248/ApkUpdater)

## 其他

+ `https://github.com/lingochamp/FileDownloader`
  + 流利说技术团队开源的Android 文件下载引擎，稳定、高效、灵活、简单易用
