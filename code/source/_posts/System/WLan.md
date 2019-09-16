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

## 命令行

+ 查看所有配置名称: `netsh wlan show profile`
+ 连接到无线WIFI: `wlan connect name=PROFILE`
  + 指定SSID: `netsh wlan connect ssid=SSID name=PROFILE`
+ 断开无线: `netsh wlan disconnect`
+ 添加配置: `Netsh WLAN add profile filename="存放路径"`
+ 导出配置：`Netsh WLAN export profile key=clear folder="存放路径"`
  + 导出的 XML 配置文件是明文存储，而且会导出 WIFI 连接密码
+ 删除配置: `Netsh WLAN delete profile name="无线名称"`
+ 无线网卡配置，状态: `Netsh WLAN show interfaces`
+ 查看指定网卡: `Netsh WLAN show interface name="网卡名称"`
+ 查看已存储密码: `Netsh WLAN show profile name="无线名称" key=clear`
+ 查看无线网卡信息: `Netsh WLAN show drivers`
+ 无线网卡兼容/支持的功能: `Netsh WLAN show wirelesscapabilities`

## 备注

+ 都是Windows标准API，懒得解释了，需要的时候直接看Demo把
+ Demo中检查到Wifi已连接时，是通过注册表获取IP数据的，实际上这个有延迟
  + 通常Windows先连接AP，然后在自动获取IP，而且获取IP整个动作是有延迟的，此时即使是使用ipconfig也未必能拿到正确的状态
  + 问题备记，搁置~~

## Demo

[WLan](https://github.com/fxliu/VCDemo/tree/master/SYSTEM/WLan)
