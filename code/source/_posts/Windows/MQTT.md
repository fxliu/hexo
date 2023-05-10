---
title: MQTT
tags: 
  - MQTT
categories: 
  - windows
description: MQTT
date: 2023-05-04 18:09:36
updated: 2023-05-04 18:09:36
---

## MQTT服务器

* [emqx](https://www.emqx.io/docs/zh/v5.0/)
  * 文档 -> 快速开始 -> 下载windows版zip包, 按照说明, 解压命令行运行即可

```sh
# 命令行: /emqx/bin/
# 启动: 指令有参数输出, 不用管, 直接HTTP访问控制台即可
emqx start
# 停止
emqx stop

# EMQX控制台
# http://localhost:18083/
# 账号: admin, 密码: public

# 访问控制 -> 认证, 添加内置数据库 -> 用户管理 -> 添加MQTT账号密码
# 管理 -> 监听器 -> 通常开启TCP即可
```

## MQTT客户端

* [MQTT](https://www.emqx.com/zh/products/mqttx)
  * 下载windows安装包即可

## MQTT使用

* 连接: 添加连接
  * 名称随意, ClientID随意
  * 服务器地址: mqtt://localhost
  * 端口: 对应tcp端口, 默认1883
  * 输入用户名密码
  * 以上, 即可连接
  
* 遗嘱
  * 必须是异常退出才会触发
  * 客户端正常退出, 不触发遗嘱

