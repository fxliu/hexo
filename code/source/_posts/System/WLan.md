---
title: 无线网卡
tags: 
  - WLAN
  - 无线网卡
categories: 
  - VC
---

## API

+ `WlanOpenHandle`: 打开操作句柄
+ `WlanEnumInterfaces`: 遍历无线设备接口，并获取接口状态
  + 已连接，连接中，已断开等
+ `WlanGetAvailableNetworkList`: 遍历热点
  + 包含SSID，加密方式等热点信息
+ `WlanGetProfileList`: 获取机器已保存所有热点配置
  + Windows没连接一次热点，会自动保存一份该热点的配置文件，配置文件名一般就是热点名
  + API操作中配置文件名可以随意指定
+ `WlanDeleteProfile`: 删除指定配置文件
+ `WlanSetProfile`: 新增/重置指定配置文件
+ `WlanConnect`: WIFI连接指令，Windows会自动查找默认配置，并尝试连接
  + 该函数指令返回时，仅说明Windows接收到该指令并开始执行，不保证能连接成功
+ `WlanDisconnect`: 终止WIFI连接

## 备注

+ 都是Windows标准API，懒得解释了，需要的时候直接看Demo把
+ Demo中检查到Wifi已连接时，是通过注册表获取IP数据的，实际上这个有延迟
  + 通常Windows先连接AP，然后在自动获取IP，而且获取IP整个动作是有延迟的，此时即使是使用ipconfig也未必能拿到正确的状态
  + 问题备记，搁置~~

## Demo

[WLan]()
