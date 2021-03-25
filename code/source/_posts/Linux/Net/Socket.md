---
title: Socket
tags: 
  - Socket
categories: 
  - linux
description: Socket
date: 2021-03-25 12:32:34
updated: 2021-03-25 12:32:34
---

## 设置接收和发送超时

```c++
struct timeval timeo = {15, 0}; // 15s
setsockopt(so, SOL_SOCKET, SO_SNDTIMEO, &timeo, sizeof(timeo));
setsockopt(so, SOL_SOCKET, SO_RCVTIMEO, &timeo, sizeof(timeo));
```
