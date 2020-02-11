---
title: WebView
tags: 
    - WebView
categories: 
    - Android
description: WebView
date: 2020-02-07 22:12:34
updated: 2020-02-07 22:12:34
---

## 基础

```xml
<!--AndroidManifest.xml：联网权限-->
<uses-permission android:name="android.permission.INTERNET"/>
```

```java
// Activity.java
mWebView.setWebViewClient(new WebViewClient() {
    // 设置在webView点击打开的新网页在当前界面显示,而不跳转到新的浏览器中
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, String url) {
        view.loadUrl(url);
        return true;
    }
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        view.loadUrl(request.getUrl().toString());
        return true;
    }
    // 页面加载完成事件
    @Override
    public void onPageFinished(WebView view, String url) {
    }
});

// 设置WebView属性,运行执行js脚本
mWebView.getSettings().setJavaScriptEnabled(true);
// 调用loadUrl方法为WebView加入链接
mWebView.loadUrl("https://www.baidu.com/");
```

## 常用API

+ `WebViewClient` 常用方法
+ `WebChromeClient` 常用方法

### 设置

+ `setAllowFileAccess` 启用或禁止WebView访问文件数据
+ `setBlockNetworkImage` 是否显示网络图像
+ `setBuiltInZoomControls` 设置是否支持缩放
+ `setCacheMode` 设置缓冲的模式
+ `setDefaultFontSize` 设置默认的字体大小
+ `setDefaultTextEncodingName` 设置在解码时使用的默认编码
+ `setFixedFontFamily` 设置固定使用的字体
+ `setJavaSciptEnabled` 设置是否支持Javascript
+ `setLayoutAlgorithm` 设置布局方式
+ `setLightTouchEnabled` 设置用鼠标激活被选项
+ `setSupportZoom` 设置是否支持缩放
+ [WebView控件之WebSettings详解](https://www.jianshu.com/p/0d7d429bd216)

### 事件

+ `doUpdate` VisitedHistory 更新历史记录
+ `onFormResubmission` 应用程序重新请求网页数据
+ `onLoadResource` 加载指定地址提供的资源
+ `onPageFinished` 网页加载完毕
+ `onPageStarted` 网页开始加载
+ `onReceivedError` 报告错误信息
+ `onScaleChanged` WebView发生改变
+ `shouldOverrideUrlLoading` 控制新的连接在当前WebView中打开
+ `onCloseWindow` 关闭WebView
+ `onCreateWindow` 创建WebView
+ `onJsAlert` 处理Javascript中的Alert对话框
+ `onJsConfirm` 处理Javascript中的Confirm对话框
+ `onJsPrompt` 处理Javascript中的Prompt对话框
+ `onProgressChanged` 加载进度条改变
+ `onReceivedlcon` 网页图标更改
+ `onReceivedTitle` 网页Title更改
+ `onRequestFocus` WebView显示焦点

## 交互

[WebView与JS交互](https://blog.csdn.net/carson_ho/article/details/64904691/)

### Android调用JS

+ 通过WebView的loadUrl（）
+ 通过WebView的evaluateJavascript（）

```html
<html>
<script type="text/javascript">
  // 使用安卓注入对象，发送消息到安卓，并接收返回值
  function sendToAndroid(msg) {
    document.getElementById("text").innerHTML = androidObject.send(msg);
  }
  // 安卓可直接调用JS函数，并反馈
  function androidCall(msg) {
    document.getElementById("text").innerHTML = msg;
    return 'ok';
  }
</script>
<body>
<input type="button" value="InWebView!" onclick="sendToAndroid('In Android land')">
<div id="text"></div>
</body>
</html>
```

```java
// 安卓调用JS androidCall函数，并接收返回值
mWebView.evaluateJavascript("javascript:androidCall('androidCall')", new ValueCallback<String>() {
    @Override
    public void onReceiveValue(String value) {
        Log.e("test", "onReceiveValue: " + value);
    }
});
// 注入JS对象，提供JS调用接口
mWebView.addJavascriptInterface(new Object() {
    @JavascriptInterface
    public String send(String msg) {
        Log.e("test", "js send: " + msg);
        return "send";
    }
}, "androidObject");
```

### JS调用Android

+ 通过`WebView`的`addJavascriptInterface()`进行对象映射
+ 通过`WebViewClient`的`shouldOverrideUrlLoading()`方法回调拦截 url
+ 通过`WebChromeClient`的`onJsAlert()`、`onJsConfirm()`、`onJsPrompt()`方法回调拦截JS对话框`alert()`、`confirm()`、`prompt()`消息
