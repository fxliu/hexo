---
title: JSON
tags: 
  - JSON
categories: 
  - linux
description: JSON
date: 2020-09-07 13:18:28
updated: 2020-09-07 13:18:28
---

## 环境

```sh
# ubuntu
sudo apt-get install libjsoncpp-dev
sudo apt remove libjsoncpp-dev

# 头文件在：/usr/include/jsoncpp/json
# 动态库在：/usr/lib/ 下搜索

# 安装后，复制 头文件 和 libjsoncpp.a 使用即可 - 卸载系统中的libjsoncpp-dev，避免编译使用错误
```

## 简单应用

```c++
// 解析
Json::Reader r;
Json::Value root;
std::string strEidJson = "{}";
if (!r.parse(strEidJson.data(), root))
{
  return FALSE;
}
// Object
Json::Value eidInfo = root.get("info", Json::stringValue);
// string
std::string strSex = eidInfo["name"].asString();
```

## Demo

`es:svn\bar_machine\trunk\C++\EIDSDK\linux\EidEsDemo`
