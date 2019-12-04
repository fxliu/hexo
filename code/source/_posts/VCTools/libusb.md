---
title: USB-HID
tags: 
  - USB
  - HID
categories: 
  - VC
description: USB, HID
date: 2019-12-03 18:01:16
updated: 2019-12-03 18:01:16
---

## 开源库

+ [libusb](https://github.com/libusb/libusb)

## 基础使用

```C++
BOOL CMyUsbHid::Init()
{
  if (libusb_init(NULL) < 0) {
    printf("SDK初始化失败");
    return FALSE;
  }
  m_devHandle = libusb_open_device_with_vid_pid(NULL, m_vid, m_pid);
  if (m_devHandle == NULL) {
    printf("设备连接失败");
    libusb_exit(NULL);
    return FALSE;
  }
  return TRUE;
}
void CMyUsbHid::Release()
{
  if (m_devHandle)
  {
    libusb_close(m_devHandle);
    libusb_exit(NULL);
    m_devHandle = NULL;
  }
}
unsigned char* CMyUsbHid::Read(int &len)
{
  ZeroMemory(m_szData, sizeof(m_szData));
  uint8_t request_type = 0xA1;  // 161
  uint8_t bRequest = 0x01;
  uint16_t wValue = 0x0100;     // 256
  uint16_t wIndex = 0x0000;

  while (true)
  {
    len = libusb_control_transfer(m_devHandle, request_type, bRequest, wValue, wIndex, m_szData, 64, 500);

    if (len < 0) {
      Log(TEXT("单片机读失败"));
      return NULL;
    }
    if (len > 0)
      break;
    Sleep(100);
  }
  return m_szData;
}
BOOL CMyUsbHid::Write(unsigned char *szData, int &len)
{
  uint8_t request_type = 0x21;  // 33
  uint8_t bRequest = 0x09;
  uint16_t wValue = 0x0200;     // 512
  uint16_t wIndex = 0x0000;

  while(len > 0)
  {
    // 这里接口有问题，只能是64，使用len会写失败
    int re = libusb_control_transfer(m_devHandle, request_type, bRequest, wValue, wIndex, szData, 64, 3000);
    if (re < 0)
    {
      Log(TEXT("单片机写失败"));
      return FALSE;
    }

    len -= 64;
    szData += 64;
  }
  return TRUE;
}
```
