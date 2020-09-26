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
// --------------------------------------------------------------------------------------
// 客户端Demo
#include "stdafx.h"
#include "MySocket.h"
#include <winsock.h>
#include <WS2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

#define MYSOCKET_OVERTIME 5000

CString Host2IP(CString strHost)
{
  addrinfo hints, *res;
  memset(&hints, 0, sizeof(addrinfo));
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_family = AF_INET;
  getaddrinfo(CW2A(strHost), NULL, &hints, &res);
  if (res)
  {
    // 可能解析出多个，直接用第一个
    TCHAR buf[256] = { 0 };
    ULONG addr = ((sockaddr_in*)(res->ai_addr))->sin_addr.s_addr;
    InetNtop(AF_INET, (PVOID)&addr, buf, sizeof(buf));
    freeaddrinfo(res);
    return buf;
  }
  return TEXT("");
}
// ----------------------------------------------------
CMySocket::CMySocket()
{
  // 全局初始化
  WORD wVersionRequested = MAKEWORD(1, 1);
  WSADATA wsaData;
  WSAStartup(wVersionRequested, &wsaData);
  m_so = SOCKET_ERROR;
}

CMySocket::~CMySocket()
{
}

BOOL CMySocket::Open(CString strIP, DWORD port)
{
  Close();
  CriticalSectionManager csm1(m_csSend);
  CriticalSectionManager csm2(m_csRecv);
  m_so = socket(AF_INET, SOCK_STREAM, 0);
  if (m_so == SOCKET_ERROR)
  {
    Close();
    return FALSE;
  }
  // Windows 是int
  int timeo = MYSOCKET_OVERTIME;
  setsockopt(m_so, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeo, sizeof(int));
  setsockopt(m_so, SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeo, sizeof(int));

  SOCKADDR_IN addrServer;
  InetPton(AF_INET, strIP, (PVOID)&addrServer.sin_addr.S_un.S_addr);
  addrServer.sin_family = AF_INET;
  addrServer.sin_port = htons(port);

  if (connect(m_so, (SOCKADDR *)&addrServer, sizeof(addrServer)) == SOCKET_ERROR)
  {
    Close();
    return FALSE;
  }
  return TRUE;
}
BOOL CMySocket::IsOpen()
{
  return m_so != SOCKET_ERROR;
}
void CMySocket::Close()
{
  if (m_so != SOCKET_ERROR)
  {
    CriticalSectionManager csm1(m_csSend);
    if (m_so != SOCKET_ERROR)
    {
      shutdown(m_so, SD_BOTH);
      closesocket(m_so);
      m_so = SOCKET_ERROR;
    }
  }
}
BOOL CMySocket::Send(char *data, int len)
{
  CriticalSectionManager csm(m_csSend);
  int res = send(m_so, data, len, 0);
  if (res != len)
    return FALSE;
  return TRUE;
}
char* CMySocket::Recv(int &len)
{
  ZeroMemory(m_szData, sizeof(m_szData));
  CriticalSectionManager csm(m_csRecv);
  len = recv(m_so, m_szData, sizeof(m_szData), 0);
  return m_szData;
}

```

## 特殊参数

### TCP_NODELAY

```C++
// 默认开启
int enable = 0;
setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, (void*)&enable, sizeof(enable));
```
