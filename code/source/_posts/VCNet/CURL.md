---
title: CURL
tags: 
  - CURL
categories: 
  - VC
description: CURL
date: 2019-12-18 16:26:15
updated: 2019-12-18 16:26:15
---

## 设置

```C++
curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 2L); // 连接超时
curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);  // 下载超时
curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L); // DNS相关优化
curl_easy_setopt(curl, CURLOPT_LOW_SPEED_LIMIT, 10L);

// CURL启动SSL参数后，执行curl_easy_perform动作时，会对本线程中TCP Socket造成干扰
// 可以通过使用单独的CURL线程避免
curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L); // 关闭SSL证书校验
curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
```
