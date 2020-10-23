---
title: JNI
tags: 
    - JNI
categories: 
    - Android
description: JNI
date: 2020-09-28 13:20:46
updated: 2020-09-28 13:20:46
---

## 资料

[Java与Native相互调用](https://www.jianshu.com/p/b71aeb4ed13d)
    + Native静态注册 - 根据JAVA类固定格式命名
    + Native动态注册 - 重写JNI_OnLoad
    + native代码反调用Java层代码
      + `GetFieldID`/`GetMethodID`：获取某个属性/某个方法
      + `GetStaticFieldID`/`GetStaticMethodID`：获取某个静态属性/静态方法
[JNI的常用方法的中文API](https://www.jianshu.com/p/67081d9b0a9c)

## DEMO

[JNI C](es:svn\bar_machine\trunk\C++\EIDSDK\Android\EsEidDemo)
