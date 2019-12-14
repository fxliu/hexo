---
title: UPNP穿透
tags: 
  - UPNP
categories: 
  - VC
description: UPNP
date: 2019-09-12 18:14:38
updated: 2019-09-12 18:14:38
---

## Socket

```C++
// Socket超时
// Windows 是 int
int timeo = 5000;
setsockopt(m_so, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeo, sizeof(int));
setsockopt(m_so, SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeo, sizeof(int));
// Linux 是 struct timeval
struct timeval timeo = { 0, 5000 };
int i = setsockopt(m_so, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeo, sizeof(timeo));
i = setsockopt(m_so, SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeo, sizeof(timeo));
```
