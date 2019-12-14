---
title: 时间
tags: 
  - time
categories: 
  - VC
description: time
date: 2019-12-12 14:09:05
updated: 2019-12-12 14:09:05
---

## 常规

```C++
// 当前时间：精确到毫秒
CString GetTime()
{
  CString strTime;
  SYSTEMTIME st;
  GetLocalTime(&st);
  strTime.Format(TEXT("[%04d-%02d-%02d %02d:%02d:%02d.%03d]"),
    st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);
  return strTime;
}
// 系统启动时长，单位：毫秒
DWORD GetTickCount();
ULONGLONG GetTickCount64();
// 程序运行时长(CPU占用时间)，单位：毫秒
// 备注：真实单位：1/CLOCKS_PER_SEC 秒, Windows 下 CLOCKS_PER_SEC=1000，相当于1ms
clock_t clock();
```
