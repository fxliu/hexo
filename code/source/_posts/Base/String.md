---
title: 字符串
tags: 
  - String
categories: 
  - VC
---

## 字符串

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

## 小函数封装

```C++
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
