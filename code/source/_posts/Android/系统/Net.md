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

```java
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.Headers;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okio.BufferedSink;

public class OkHttpUtil {
    private static String TAG = OkHttpUtil.class.getSimpleName();
    private static OkHttpClient client = new OkHttpClient();

    public static void startSync(final Request request) {
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
    }

    public static void start(final Request request) {
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
    }

    public static Request getRequest(String url) {
        RequestBody requestBody = new FormBody.Builder()
                .add("search", "lala")
                .build();
        return new Request.Builder()
                .url("url")
                .get()      // 默认get
                .build();
    }

    public static Request myHeaderRequest(String url) {
        // 自定义头
        return new Request.Builder()
                .url("url")
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
                .url("https://testurl")
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
        OkHttpClient okHttpClient = new OkHttpClient();
        RequestBody requestBody = new FormBody.Builder()
                .add("search", "Jurassic Park")
                .build();
        return new Request.Builder()
                .url("https://en.wikipedia.org/w/index.php")
                .post(requestBody)
                .build();
    }
}
```

## APP升级

+ [AutoUpdateProject](https://github.com/MZCretin/AutoUpdateProject)
