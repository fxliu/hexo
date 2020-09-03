---
title: USBHID
tags: 
  - USBHID
categories: 
  - VC
description: USBHID
date: 2019-12-23 18:32:50
updated: 2019-12-23 18:32:50
---

## 工具

+ 抓包工具：`Bus Hound`
+ 开源封装：[libusb](https://github.com/libusb/libusb)
+ [hidapi](https://github.com/libusb/hidapi)

## libusb 简单使用

```C++
// es:svn\bar_machine\trunk\C++\Demo\IdCardServerEx
BOOL CMyUsbHid::Init()
{
  if (m_devHandle)
    return TRUE;
  CriticalSectionManager csm(m_cs);
  CUsbHidConfig cfg;
  m_vid = 0x0400;     // 未知的话，可以使用遍历函数，遍历所有
  m_pid = 0x9666;
  if (libusb_init(NULL) < 0) {
    LOG_HID_ERROR(TEXT("SDK初始化失败"));
    return FALSE;
  }
  m_devHandle = libusb_open_device_with_vid_pid(NULL, m_vid, m_pid);
  if (m_devHandle == NULL) {
    LOG_HID_ERROR(TEXT("设备连接失败"));
    libusb_exit(NULL);
    return FALSE;
  }
  if (!IsModule())
  {
    if (libusb_set_configuration(m_devHandle, 1) < 0) {
      LOG_HID_ERROR(TEXT("设备配置失败"));
      libusb_exit(NULL);
      return FALSE;
    }

    if (libusb_claim_interface(m_devHandle, 0) < 0) {
      LOG_HID_ERROR(TEXT("设备接口打开失败"));
      libusb_exit(NULL);
      return FALSE;
    }
  }
  //PrintInfo();
  return TRUE;
}
BOOL CMyUsbHid::CheckInit()
{
  return m_devHandle != NULL;
  }
void CMyUsbHid::Release()
{
  if (m_devHandle)
  {
    CriticalSectionManager csm(m_cs);
    libusb_close(m_devHandle);
    libusb_exit(NULL);
    m_devHandle = NULL;
  }
}
// 命令字方式读取
int CMyUsbHid::ReadModule(unsigned char* szData)
{
  // 指令
  uint8_t request_type = 0xA1;  // 161
  uint8_t bRequest = 0x01;
  uint16_t wValue = 0x0100;     // 256
  uint16_t wIndex = 0x0000;

  CriticalSectionManager csm(m_cs);
  return libusb_control_transfer(m_devHandle, request_type, bRequest, wValue, wIndex, szData, 64, 500);
}
unsigned char* CMyUsbHid::Read(int &len)
{
  ZeroMemory(m_szData, sizeof(m_szData));
  // TODO: 在此添加控件通知处理程序代码
  unsigned char epIn = 0x84;  // 常规读终端地址, 可查询接口属性获取 endpoint_in
  int packLen = 0x0040;       // 64，包长度
  unsigned char *szTmp = m_szData;
  while (TRUE)
  {
    if (!m_devHandle)
    {
      len = -1;
      LOG_HID_ERROR(L"单片机读失败: need init");
      return NULL;
    }
    // transfer type: interrupt
    int tmpLen = 0;
    int re = 0;
    if (IsModule())
      re = tmpLen = ReadModule(szTmp);
    else
      re = libusb_interrupt_transfer(m_devHandle, epIn, szTmp, packLen, &tmpLen, 500);
    // transfer type: bulk
    //int re = libusb_interrupt_transfer(m_devHandle, epIn, szTmp, packLen, &tmpLen, 2000);
    if (re < 0 && re != LIBUSB_ERROR_TIMEOUT) {
      len = -1;
      LOG_HID_ERROR(L"单片机读失败: %d, need init", re);
      return NULL;
    }
    if (tmpLen == 0) {
      return NULL;
    }
    if (len == 0)
    {
      // 当前帧数据长度
      len = szTmp[4];
      len <<= 8;
      len += szTmp[5];
      len += 8;
      if (len < packLen)
        break;
    }
    szTmp += packLen;
    if (szTmp - m_szData > len)
      break;
  }
  return m_szData;
}
int CMyUsbHid::WriteModule(unsigned char *szData, int len)
{
  // 控制字写
  uint8_t request_type = 0x21;  // 33
  uint8_t bRequest = 0x09;
  uint16_t wValue = 0x0200;     // 512
  uint16_t wIndex = 0x0000;

  return libusb_control_transfer(m_devHandle, request_type, bRequest, wValue, wIndex, szData, len, 3000);
}
BOOL CMyUsbHid::Write(unsigned char *szData, int len)
{
  CriticalSectionManager csm(m_cs);
  int lenTmp = len;
  unsigned char *szDataTmp = szData;
  int packLen = 0x0040;         // 64
  while(lenTmp > 0)
  {
    if (!m_devHandle)
      return FALSE;

    int epOut = 0x03;  // 常规写终端地址，可查询接口属性获取 endpoint_out
    int actual_length = 0;
    int re = 0;
    if (IsModule())
    {
      re = WriteModule(szDataTmp, packLen);
      actual_length = packLen + 1;
    }
    else
      re = libusb_interrupt_transfer(m_devHandle, epOut, szDataTmp, packLen, &actual_length, 1000);
    if ((re < 0) || (actual_length != packLen+1))
    {
      LOG_HID_ERROR(TEXT("单片机写失败:re=%d, packLen=%d, actual_length=%d"), re, packLen, actual_length);
      return FALSE;
    }
    else
    {
      //LOG_HID_DEBUG(TEXT("单片机写成功:re=%d, packLen=%d"), re, packLen);
    }

    lenTmp -= packLen;
    szDataTmp += packLen;
  }
  if (len > 1000)
  {
    LOG_HID_DEBUG(TEXT("大包解析延迟5ms"));
    Sleep(5);
  }
  return TRUE;
}
```

## windows 环境

`es:svn\bar_machine\trunk\C++\Demo\EidEsDemo`

## linux 环境

```sh
# 见README.md
# 失败情况：一版时缺对应库，yum安装即可
# sudo apt-get install libudev-dev libusb-1.0-0-dev libfox-1.6-dev
# sudo apt-get install autotools-dev autoconf automake libtool
./bootstrap
./configure
make
make install # as root, or using sudo

# libudev-dev
# on ubuntu： apt-get install libudev-dev
# on centos： yum install systemd-devel
```
