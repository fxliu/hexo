---
title: 字符串
tags: 
  - String
categories: 
  - VC
description: String
date: 2019-10-10 15:21:28
updated: 2019-10-10 15:21:28
---

## 小函数封装

```C++
#include<shlwapi.h>
CString GetRunPath()
{
    TCHAR szPath[MAX_PATH] = {0};
    GetModuleFileName(NULL,szPath,sizeof(szPath));
    PathRemoveFileSpec(szPath);
    return szPath;
}
```

```C++
// UNICODE 编码转换
char H2I(char ch)
{
  if (ch >= '0' && ch <= '9')
    return ch - '0';
  if (ch >= 'a' && ch <= 'f')
    return ch - 'a' + 10;
  return ch - 'A' + 10;
}
// "A\u5218B" -> A刘B
CStringA Uncode2String(char *d)
{
  CStringA str;
  while(*d)
  {
    if (strlen(d) < 6)
    {
      str += d;
      break;
    }
    if (d[0] == '\\' && d[1] == 'u')
    {
      WCHAR ch[2] = { 0 };
      ch[0] = (WCHAR((H2I(d[2]) << 4) + H2I(d[3])) << 8) + (H2I(d[4]) << 4) + H2I(d[5]);
      // CP_UTF8
      str += CW2A(ch);
      d += 6;
    }
    else
    {
      str += d[0];
      d += 1;
    }
  }
  return str;
}
```
