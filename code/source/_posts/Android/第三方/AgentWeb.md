---
title: AgentWeb
tags: 
    - AgentWeb
categories: 
    - Android
description: AgentWeb
date: 2020-02-23 08:49:51
updated: 2022-08-14 11:28:48
---

## 基础

[AgentWeb-GitHub-包含Demo](https://github.com/Justson/AgentWeb)

* 封装: svn\cloud_visitor\trunk\4_android\guard
  * AgentWebUtil: AgentWeb + jsbridge
* 封装: svn\esface\trunk\Android\recognise
  * AgentWebFragment: AgentWeb + jsbridge

## 引入

```groovy
allprojects {
	repositories {
		...
		maven { url 'https://jitpack.io' }
	}
}
```

+ Support: 参照官方文档

```groovy
// Support
implementation 'com.github.Justson.AgentWeb:agentweb-core:v5.0.0-alpha' // (必选)
implementation 'com.github.Justson.AgentWeb:agentweb-filechooser:v5.0.0-alpha' // (可选)
implementation 'com.github.Justson:Downloader:v5.0.0' // (可选)
// AgentWeb会尝试加载所有组件，可选功能没有时，会报错，忽略即可
```

+ Androidx: 参照官方文档

```groovy
 implementation 'com.github.Justson.AgentWeb:agentweb-core:v5.0.0-alpha.1-androidx' // (必选)
 implementation 'com.github.Justson.AgentWeb:agentweb-filechooser:v5.0.0-alpha.1-androidx' // (可选)
 implementation 'com.github.Justson:Downloader:v5.0.0-androidx' // (可选)
```

+ 权限申请: 参照官方Demo

```groovy
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
<uses-permission android:name="android.permission.READ_PHONE_STATE"/>
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
```

+ 混淆: 参照官方Demo

```pro
# release 编译混淆告警处理
# 依赖的第三方库，取消混淆即可
-dontwarn com.download.library.**
-keep class com.download.library.** { *; }

-dontwarn com.alipay.sdk.**
-keep class com.alipay.sdk.** { *; }
```

```makefile
# 取消AgentWeb混淆
-keep class com.just.agentweb.** {
    *;
}
-dontwarn com.just.agentweb.**
```

## AgentWeb使用

```java
// 参照Demo AgentWebFragment 创建 AgentWeb 对象, 并绑定到指定 View
// 当前Demo中只有这里的创建有完整说明, 需要其他功能时, 在从Demo中获取
AgentWeb.with()				// 绑定主窗体 Activity/Fragment
    .setAgentWebParent()	// Web上层父控件 Layout, 并设定LayoutParams参数
    // IAgentWebSettings继承android.webkit.WebSettings, 应该用于WebView基础属性设定, 例如文字大小之类
    // 可以忽略不设置
    .setAgentWebWebSettings()
    // 拦截页面事件, 开始打开/打开完成 等
    .setWebViewClient()
    // 设置WebViewClient中间件，支持多个WebViewClient, 可以屏蔽
    .useMiddlewareWebClient()
    // 拦截页面加载过程事件, 例如页面加载进度条, 获取Title等
    .setWebChromeClient()
    // 设置WebChromeClient中间件，支持多个WebChromeClient, 可以屏蔽
    .useMiddlewareWebChrome()
    // 各种UI效果重置, 弹窗等
    // 注意拦截错误页时, 需要自行处理 onMainFrameError 事件
    .setAgentWebUIController()
    // 建议配置, 这个是JS编写要求
    .setSecurityType(AgentWeb.SecurityType.STRICT_CHECK)
    // 错误页显示内容, 研发调试最好按照Demo配置下
    .setMainFrameErrorView(com.just.agentweb.R.layout.agentweb_error_page, -1)
    // HTTP通讯头, 可以设置cookie等
    .additionalHttpHeader()
    // 页面跳转处理: 打开其他页面时，弹窗质询用户前往其他应用
    .setOpenOtherPageWays()
    // 拦截找不到相关页面的Url
    .interceptUnkownUrl()
    .createAgentWeb()	//创建AgentWeb。
    .ready()			//设置 WebSettings。
    .go("https://www.baidu.com");

// Debug模式
AgentWebConfig.debug();
// 其他 功能函数
mAgentWeb.clearWebCache();	// 清空缓存
// AgentWeb 没有把WebView的功能全面覆盖 ，所以某些设置 AgentWeb 没有提供 ， 请从WebView方面入手设置。
mAgentWeb.getWebCreator().getWebView().setOverScrollMode(WebView.OVER_SCROLL_NEVER);
// 设置透明 - 注意Web上面有一层 Layout
mAgentWeb.getWebCreator().getWebView().setBackgroundColor(0x00000000);
mAgentWeb.getWebCreator().getWebParentLayout().setBackgroundColor(0x00000000);
```

## jsbridge

* `implementation 'com.github.lzyzsd:jsbridge:1.0.4'`
* 控制台消息

```java
// JS控制台日志接收: console.log('msg');
protected com.just.agentweb.WebChromeClient mWebChromeClient = new WebChromeClient() {
    @Override
    public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
        @SuppressLint("DefaultLocale")
        String msg = String.format("%s(%d): %s", consoleMessage.sourceId(),
                                   consoleMessage.lineNumber(), consoleMessage.message());
        if (consoleMessage.sourceId().isEmpty() && consoleMessage.message().indexOf("\"responseData\"") > 0) {
            Log.e("JsBridge: ", msg);
        } else {
            Log.e("onConsoleMessage", msg);
        }
        return true;
    }
};
```

* jsbridge 挂载

```java
// 变量定义
private BridgeWebView mBridgeWebView;
mBridgeWebView = new BridgeWebView(getContext());
// AgentWeb绑定
AgentWeb.with()
    ...
    .setWebViewClient(getWebViewClient())
	.setWebView(mBridgeWebView)
    ...;
// 注意重写 WebViewClient, 
// 参照 JsbridgeWebFragment, 拦截关键事件把 mBridgeWebView 绑定到当前页面即可
private WebViewClient getWebViewClient() {
    return new WebViewClient() {
        BridgeWebViewClient mBridgeWebViewClient = new BridgeWebViewClient(mBridgeWebView);

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            if (mBridgeWebViewClient.shouldOverrideUrlLoading(view, url)) {
                return true;
            }
            return super.shouldOverrideUrlLoading(view, url);
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                if (mBridgeWebViewClient.shouldOverrideUrlLoading(view, request.getUrl().toString())) {
                    return true;
                }
            }
            return super.shouldOverrideUrlLoading(view, request);
        }

        @Override
        public void onPageStarted(WebView view, String url, Bitmap favicon) {
            super.onPageStarted(view, url, favicon);
        }

        @Override
        public void onPageFinished(WebView view, String url) {
            super.onPageFinished(view, url);
            mBridgeWebViewClient.onPageFinished(view, url);
        }
    };
}
```

* jsbridge Java端初始化: 必须在页面加载前调用

```java
// 对应 WebViewJavascriptBridge.init 回调
mBridgeWebView.send("hello", new CallBackFunction() {
    public void onCallBack(String data) {
        Log.e(TAG, "BridgeWebView.send CallBackFunction: " + data);
    }
});
// 指定 函数
mBridgeWebView.callHandler("functionInJs", new Gson().toJson("hello"), new CallBackFunction() {
    @Override
    public void onCallBack(String data) {
        Log.e(TAG, "callHandler(functionInJs) onCallBack: " + data);
    }
});
```

* jsbridge JS端初始化: 

```js
// 连接函数
function connectWebViewJavascriptBridge(callback) {
    if (window.WebViewJavascriptBridge) {
        callback(WebViewJavascriptBridge)
    } else {
        document.addEventListener(
            'WebViewJavascriptBridgeReady'
            , function() {
                callback(WebViewJavascriptBridge)
            },
            false
        );
    }
}
// 指定连接回调 - 必须在JS初始加载时运行
connectWebViewJavascriptBridge(function(bridge) {
    // 对应 BridgeWebView.send
    bridge.init(function(message, responseCallback) {
        console.log('bridge.init:', message);
        responseCallback('ok');
    });
	// 对应 BridgeWebView.callHandler
    bridge.registerHandler("functionInJs", function(data, responseCallback) {
        bridgeLog("data from Java:" + data);
        responseCallback('ok');
    });
})
/* 执行顺序
0. Java端执行 send + callHandler
1. onPageFinished: 页面加载完成
2. JS消息 bridge.init:  hello
3. JS消息 functionInJs:  hello
4. Java BridgeWebView.send 收到 执行结果回调
5. Java BridgeWebView.callHandler 收到 执行结果回调
*/
```

* WebViewJavascriptBridge 通讯: Java端

```java
// 默认回调: 对应 window.WebViewJavascriptBridge.send
mBridgeWebView.setDefaultHandler(new BridgeHandler() {
    public void handler(String data, CallBackFunction function) {
        Log.e(TAG, "BridgeWebView(DefaultHandler): " + data);
        function.onCallBack("ok");
    }
});
// 命名回调: 对应 window.WebViewJavascriptBridge.callHandler
mBridgeWebView.registerHandler("functionInJava", new BridgeHandler() {
    @Override
    public void handler(String data, CallBackFunction function) {
        Log.e(TAG, "functionInJava: " + data);
        function.onCallBack("ok");
    }
});
```

* WebViewJavascriptBridge 通讯: JS端

```html
<div><input type="button" id="enter" value="发消息给Native" onclick="testClick();"/></div>
<div><input type="button" id="enter1" value="调用Native方法" onclick="testClick1();"/></div>

<script language="JavaScript">
    function testClick() {
        window.WebViewJavascriptBridge.send(
            'hello',			// 发送内容: 字符串 / 对象
            function(responseData) {
                 console.log("send result:", responseData)
            }
        );
    }
    function testClick1() {
        window.WebViewJavascriptBridge.callHandler(
            'functionInJava',	// 指定 Java 注册函数名
            'hello',			// 发送内容: 字符串 / 对象
            function(responseData) {
                 console.log("callHandler result:", responseData)
            }
        );
    }
</script>
```

* 定义专有通讯: Java端

```java
private JsAccessEntrace js;
this.js = mAgentWeb.getJsAccessEntrace();
// 定义对象, 注册回调函数
class AndroidInterface {
    @JavascriptInterface
    public String onTest(String msg) {
        Log.e(TAG, "AndroidInterface.onTest: " + msg);
        return "ok";
    }
}
// 注入对象到JS: 可以在页面加载前预注入
mAgentWeb.getJsInterfaceHolder().addJavaObject("androidObj", new AndroidInterface());

// 调用 JS 函数: 必须在页面加载完成之后调用
js.quickCallJs(
    "JSCommand.onTest",					// 指定 JS函数
    new ValueCallback<String>() {	    // 返回值接收回调
        @Override
        public void onReceiveValue(String value) {
            Log.i(TAG, "quickCallJs onReceiveValue: " + value);
        }
    }, "hello"							// JS函数参数, 支持多个, 支持Json对象
);
```

* 定义专有通讯: Js 端 - 必须在页面加载完成之后调用

```js
// inter_js.js
// JS接口, 定义 对象/函数 提供 Java 调用
JSCommand = {};
JSCommand.onTest = function(data) {
    console.log('JSCommand.onTest:', data);
    return 'ok';
}

// inter_java.js
// 调用 Java 注入对象, 并打印返回值
function android_onLog() {
    console.log('JSCommand.onTest:', androidObj.onTest("hello"));
}
```

