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

```gradle
// build.gradle(app)
implementation 'com.just.agentweb:agentweb:4.1.2' // (必选)
implementation 'com.just.agentweb:filechooser:4.1.2'// (可选)
implementation 'com.download.library:Downloader:4.1.2'// (可选)
// Demo\sample\libs目录有 alipaySdk-20180601.jar // (可选)
// AgentWeb会尝试加载所有组件，可选功能没有时，会报错，忽略即可
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

## 使用

```java
// 附加对象从Demo获取即可
AgentWeb mAgentWeb;
public void Init(AppCompatActivity app) {
    mAgentWeb = AgentWeb.with(app)
            .setAgentWebParent((LinearLayout) app.findViewById(R.id.webLayout), new LinearLayout.LayoutParams(-1, -1))
            .useDefaultIndicator()
            .setAgentWebWebSettings(new CustomSettings())
            .setWebChromeClient(mWebChromeClient)
            .setWebViewClient(mWebViewClient)
            .setAgentWebUIController(mAgentWebUIController)
            .setMainFrameErrorView(R.layout.agentweb_error_page, -1)
            .setSecurityType(AgentWeb.SecurityType.STRICT_CHECK)
            .setWebLayout(new WebLayout(app))
            .setOpenOtherPageWays(DefaultWebClient.OpenOtherPageWays.ASK)//打开其他应用时，弹窗咨询用户是否前往其他应用
            .interceptUnkownUrl() //拦截找不到相关页面的Scheme
            .createAgentWeb()
            .ready()
            .go(Config.WebUrl.get(app));
    addBGChild((FrameLayout) mAgentWeb.getWebCreator().getWebParentLayout());
}

private com.just.agentweb.WebViewClient mWebViewClient = new WebViewClient() {
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        return super.shouldOverrideUrlLoading(view, request);
    }

        @Override
        public void onPageStarted(WebView view, String url, Bitmap favicon) {
            super.onPageStarted(view, url, favicon);
            Log.i(TAG, "onPageStarted: " + url);
            if(mIsMainFrameError) {
                // 错误页隐藏，源码这里处理有漏洞
                // 当遇到页面跳转时：onPageStarted中的url和onPageFinished的url可能不一致
                // 源码校验url必须一致才会隐藏错误页
                // 自己强制处理下
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
        Log.i(TAG, "onMainFrameError: " + failingUrl);
        mIsMainFrameError = true;
    }
};
```
