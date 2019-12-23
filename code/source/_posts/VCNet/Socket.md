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

// 全局初始化
WORD wVersionRequested = MAKEWORD(1, 1);
WSADATA wsaData;
WSAStartup(wVersionRequested, &wsaData);
m_so = SOCKET_ERROR;

// 客户端Demo
BOOL CHidServer::Open()
{
  Close();
  CriticalSectionManager csm1(m_csSend);
  CriticalSectionManager csm2(m_csRecv);
  m_so = socket(AF_INET, SOCK_STREAM, 0);
  if (m_so == SOCKET_ERROR)
  {
    LOG_HID_ERROR(TEXT("Socket 创建失败"));
    Close();
    return FALSE;
  }
  // Windows 是int
  int timeo = 5000;
  setsockopt(m_so, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeo, sizeof(int));
  setsockopt(m_so, SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeo, sizeof(int));

  SOCKADDR_IN addrServer;
  InetPton(AF_INET, "127.0.0.1", (PVOID)&addrServer.sin_addr.S_un.S_addr);
  addrServer.sin_family = AF_INET;
  addrServer.sin_port = htons(8080);

  if (connect(m_so, (SOCKADDR *)&addrServer, sizeof(addrServer)) == SOCKET_ERROR)
  {
    Close();
    LOG_HID_ERROR(TEXT("Socket 连接解码器失败"));
    return FALSE;
  }
  LOG_HID_DEBUG(TEXT("Socket(TCP) 连接成功"));
  return TRUE;
}
BOOL CHidServer::IsOpen()
{
  return m_so != SOCKET_ERROR;
}
void CHidServer::Close()
{
  if (m_so != SOCKET_ERROR)
  {
    CriticalSectionManager csm1(m_csSend);
    if (m_so != SOCKET_ERROR)
    {
      shutdown(m_so, SD_BOTH);
      closesocket(m_so);
      m_so = SOCKET_ERROR;
      LOG_HID_DEBUG(TEXT("Socket(TCP) 链接关闭"));
    }
  }
}

BOOL CHidServer::Send(char *data, int len)
{
  CriticalSectionManager csm(m_csSend);
  int res = send(m_so, data, len, 0);
  if (res != len)
  {
    LOG_HID_ERROR(TEXT("socket发送数据到解码器失败"));
    return FALSE;
  }
  return TRUE;
}

char* CHidServer::Recv(int &len)
{
  ZeroMemory(m_szData, sizeof(m_szData));
  CriticalSectionManager csm(m_csRecv);
  len = recv(m_so, m_szData, sizeof(m_szData), 0);
  if (len < 0)
  {
    LOG_HID_ERROR(TEXT("recv异常"));
    return NULL;
  }
  if(len == 0)
    LOG_HID_ERROR(TEXT("recv空数据"));
  return m_szData;
}

```
