---
title: AgentWeb
tags: 
    - AgentWeb
categories: 
    - Android
description: AgentWeb
date: 2020-02-23 08:49:51
updated: 2020-02-23 08:49:51
---

## 基础

[AgentWeb-GitHub-包含Demo](https://github.com/Justson/AgentWeb)

## 引入

```gradle
allprojects {
	repositories {
		...
		maven { url 'https://jitpack.io' }
	}
}
```

```gradle
// Support
 implementation 'com.github.Justson.AgentWeb:agentweb-core:v5.0.0-alpha' // (必选)
 implementation 'com.github.Justson.AgentWeb:agentweb-filechooser:v5.0.0-alpha' // (可选)
 implementation 'com.github.Justson:Downloader:v5.0.0' // (可选)
// AgentWeb会尝试加载所有组件，可选功能没有时，会报错，忽略即可
```

```gradle
// Androidx
 implementation 'com.github.Justson.AgentWeb:agentweb-core:v5.0.0-alpha.1-androidx' // (必选)
 implementation 'com.github.Justson.AgentWeb:agentweb-filechooser:v5.0.0-alpha.1-androidx' // (可选)
 implementation 'com.github.Justson:Downloader:v5.0.0-androidx' // (可选)
```

```pro
# release 编译混淆告警处理
# 依赖的第三方库，取消混淆即可
-dontwarn com.download.library.**
-keep class com.download.library.** { *; }

-dontwarn com.alipay.sdk.**
-keep class com.alipay.sdk.** { *; }

-dontwarn me.nereo.multi_image_selector.**
-keep class me.nereo.multi_image_selector.** { *; }
```

```makefile
# 取消AgentWeb混淆
-keep class com.just.agentweb.** {
    *;
}
-dontwarn com.just.agentweb.**
```

## 使用

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:id="@+id/webLayout"
    tools:context=".WebActivity">

</LinearLayout>
```

```java
public class AgentWebUtil {
    private static String TAG = AgentWebUtil.class.getSimpleName();
    private static AgentWebUtil mAgentWebUtil;
    AgentWeb.PreAgentWeb mPreAgentWeb;
    private AgentWeb mAgentWeb;
    private AlertDialog mAlertDialog;
    private AppCompatActivity app;
    private boolean mIsFinish = false;
    private boolean mIsMainFrameError = false;
    // ------------------------------------------------------------------------
    public void init(AppCompatActivity app) {
        AgentWebUtil.mAgentWebUtil = this;
        this.app = app;
        mPreAgentWeb = AgentWeb.with(app)
                .setAgentWebParent((LinearLayout) app.findViewById(R.id.webLayout), new LinearLayout.LayoutParams(-1, -1))
                .useDefaultIndicator() //设置进度条颜色与高度，-1为默认值，高度为2，单位为dp。
                .setAgentWebWebSettings(new CustomSettings()) //设置 IAgentWebSettings。
                .setWebChromeClient(mWebChromeClient)
                .setWebViewClient(mWebViewClient)
                .setPermissionInterceptor(mPermissionInterceptor) //权限拦截 2.0.0 加入。
                .setAgentWebUIController(mAgentWebUIController) //自定义UI  AgentWeb3.0.0 加入
                .setMainFrameErrorView(R.layout.agentweb_error_page, -1)
                .setSecurityType(AgentWeb.SecurityType.STRICT_CHECK)
                // .setWebLayout(new WebLayout(app)) // 下拉刷新显示内容
                .setOpenOtherPageWays(DefaultWebClient.OpenOtherPageWays.ASK)//打开其他应用时，弹窗咨询用户是否前往其他应用
                .interceptUnkownUrl() //拦截找不到相关页面的Scheme
                .createAgentWeb();

        mAgentWeb = mPreAgentWeb.get();
        mAgentWeb.clearWebCache();
        AgentWebConfig.debug();
        mAgentWeb.getWebCreator().getWebView().setOverScrollMode(WebView.OVER_SCROLL_NEVER);
        mPreAgentWeb.go(Config.WebUrl.get(app));
        addBGChild((FrameLayout) mAgentWeb.getWebCreator().getWebParentLayout());
    }

    public AgentWeb Web() {
        return mAgentWeb;
    }
    public boolean IsFinish() {
        return mIsFinish;
    }
    public void go(String url){
        mPreAgentWeb.go(url);
    };

    private com.just.agentweb.WebChromeClient mWebChromeClient = new WebChromeClient() {
        @Override
        public void onReceivedTitle(WebView view, String title) {
            super.onReceivedTitle(view, title);
        }
        @Override
        public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
            Log.e("onConsoleMessage",  String.format("%s(%d): %s", consoleMessage.sourceId(),
                    consoleMessage.lineNumber(), consoleMessage.message()));
            return true;
        }
    };
    private com.just.agentweb.WebViewClient mWebViewClient = new WebViewClient() {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            return super.shouldOverrideUrlLoading(view, request);
        }

        @Override
        public void onPageStarted(WebView view, String url, Bitmap favicon) {
            super.onPageStarted(view, url, favicon);
            Log.i(TAG, "onPageStarted: " + url);
            // 错误页隐藏，源码这里处理有漏洞
            // 当遇到页面跳转时：onPageStarted中的url和onPageFinished的url可能不一致
            // 源码校验url必须一致才会隐藏错误页
            // 自己强制处理下
            if(mIsMainFrameError) {
                mAgentWebUIController.onShowMainFrame();
                mIsMainFrameError = false;
            }
        }
        @Override
        public void onPageFinished(WebView view, String url) {
            super.onPageFinished(view, url);
            Log.i(TAG, "onPageFinished: " + url);
            mIsFinish = true;
        }
    };
    private AgentWebUIControllerImplBase mAgentWebUIController = new AgentWebUIControllerImplBase() {
        @Override
        public void onMainFrameError(WebView view, int errorCode, String description, String failingUrl) {
            super.onMainFrameError(view, errorCode, description, failingUrl);
            Log.e(TAG, "onMainFrameError: " + failingUrl);
            mIsMainFrameError = true;
        }
    };
    protected PermissionInterceptor mPermissionInterceptor = new PermissionInterceptor() {

        /**
         * PermissionInterceptor 能达到 url1 允许授权， url2 拒绝授权的效果。
         * @return true 该Url对应页面请求权限进行拦截 ，false 表示不拦截。
         */
        @Override
        public boolean intercept(String url, String[] permissions, String action) {
            Log.i(TAG, "mUrl:" + url + "  permission:" + new Gson().toJson(permissions) + " action:" + action);
            return false;
        }
    };

    private void addBGChild(FrameLayout frameLayout) {
        TextView mTextView = new TextView(frameLayout.getContext());
        mTextView.setText("技术由 哈尔滨赛奥科技 提供");
        mTextView.setTextSize(16);
        mTextView.setPadding(10, 20, 10, 0);
        mTextView.setTextColor(Color.parseColor("#727779"));
        frameLayout.setBackgroundColor(Color.parseColor("#272b2d"));
        FrameLayout.LayoutParams mFlp = new FrameLayout.LayoutParams(-2, -2);
        mFlp.gravity = Gravity.CENTER_HORIZONTAL;
        final float scale = frameLayout.getContext().getResources().getDisplayMetrics().density;
        mFlp.topMargin = (int) (15 * scale + 0.5f);
        frameLayout.addView(mTextView, 0, mFlp);
    }

    public void showDialog(final AppCompatActivity app) {
        if (mAlertDialog == null) {
            mAlertDialog = new AlertDialog.Builder(app)
                    .setMessage("您确定要关闭该页面吗?")
                    .setNegativeButton("再逛逛", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            if (mAlertDialog != null) {
                                mAlertDialog.dismiss();
                            }
                        }
                    })
                    .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            if (mAlertDialog != null) {
                                mAlertDialog.dismiss();
                            }
                            app.finish();
                        }
                    }).create();
        }
        mAlertDialog.show();
    }
}
```

## jsbridge

`implementation 'com.github.lzyzsd:jsbridge:1.0.4'`

```js
function $(objId) {
    return document.getElementById(objId);
}
//注册事件监听，初始化
function setupWebViewJavascriptBridge(callback) {
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
//回调函数，接收java发送来的数据
setupWebViewJavascriptBridge(function(bridge) {
   // 默认接收
   bridge.init(function(msg, responseCallback) {
        $("msg").innerHTML = msg;
        responseCallback("ok"); //回传数据给java
   });

   // 指定接收，参数 java 保持一致
   bridge.registerHandler("jsTestFunc", function(msg, responseCallback) {
        $("msg").innerHTML = msg;
        responseCallback("ok"); //回传数据给java
   });
})
// 发送数据
<button style="width:30%;" type="button" onclick="send();">打开蓝牙</button>
function android_bleOpen() {
    // 发送数据到 java 默认接口，反馈数据一定是字符串，Json不会被自动转换为对象
    window.WebViewJavascriptBridge.send(
        "from js msg"
        , function(responseData) {
            $("msg").innerHTML = responseData;
        }
    );
    // 发送数据到 java 指定接口
    window.WebViewJavascriptBridge.callHandler(
        'javaTestFunc'
        , "hello"
        , function(responseData) {
            $("msg").innerHTML = responseData;
        }
    );
}
```

```java
public class AgentWebUtil {
    private AgentWeb.PreAgentWeb mPreAgentWeb;

    public void init(AppCompatActivity app) {
        mBridgeWebView = new BridgeWebView(app);
        mAgentWeb = AgentWeb.with(this)
                .setWebViewClient(getWebViewClient())
                // ...
                .go(getUrl());
        // 默认接收
        mBridgeWebView.setDefaultHandler(new BridgeHandler() {
            public void handler(String data, CallBackFunction function) {
                Log.e(TAG, data);
                function.onCallBack("ok");
            }
        });
        // 指定接收
        mBridgeWebView.registerHandler("javaTestFunc", new BridgeHandler() {
            @Override
            public void handler(String data, CallBackFunction function) {
                function.onCallBack("ok");
            }
        });
        // 默认发送
        mBridgeWebView.send("hello", new CallBackFunction(){
            public void onCallBack(String data) {
                Log.e(TAG, "反馈：" + data);
            }
        });
        // 指定发送
        mBridgeWebView.callHandler("jsTestFunc", new Gson().toJson(user), new CallBackFunction() {
            @Override
            public void onCallBack(String data) {
                Log.e(TAG, "反馈：" + data);
            }
        });
    }
    private WebViewClient getWebViewClient() {
        return new WebViewClient() {
            // 事件拦截
            BridgeWebViewClient mBridgeWebViewClient = new BridgeWebViewClient(mBridgeWebView);
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return mBridgeWebViewClient.shouldOverrideUrlLoading(view, request.getUrl().toString());
                // return super.shouldOverrideUrlLoading(view, request);
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
    };
}
```
