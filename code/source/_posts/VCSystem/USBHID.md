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

## 简单使用

```C++
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
void CMyUsbHid::PrintInfo()
{
  libusb_device *dev = libusb_get_device(m_devHandle);
  // 读取设备属性 Device properties
  uint8_t bus = libusb_get_bus_number(dev);
  uint8_t port_path[8];
  int port_numbers = libusb_get_port_numbers(dev, port_path, sizeof(port_path));
  if (port_numbers > 0) {
    LOG_HID_DEBUG(TEXT("Device properties:"));
    LOG_HID_DEBUG(TEXT("\tbus number: %d"), bus);
    CString strPortPath;
    strPortPath.Format(TEXT("\tport path: %d"), port_path[0]);
    for (int i = 1; i < port_numbers; i++) {
      CString strTmp;
      strTmp.Format(TEXT("->%d"), port_path[i]);
      strPortPath += strTmp;
    }
    LOG_HID_DEBUG(strPortPath);
    //LOG_HID_DEBUG(TEXT(" (from root hub)"));
  }
  int speed = libusb_get_device_speed(dev);
  if ((speed < 0) || (speed > 4))
    speed = 0;
  static TCHAR *speed_name[5] = { L"Unknown", L"1.5 Mbit/s (USB LowSpeed)", L"12 Mbit/s (USB FullSpeed)",
    L"480 Mbit/s (USB HighSpeed)", L"5000 Mbit/s (USB SuperSpeed)" };
  LOG_HID_DEBUG(L"\tspeed: %s", speed_name[speed]);

  // 读取设备描述 Reading device descriptor
  struct libusb_device_descriptor dev_desc;
  if (libusb_get_device_descriptor(dev, &dev_desc) >= 0)
  {
    LOG_HID_DEBUG(TEXT("Reading device descriptor:"));
    LOG_HID_DEBUG(L"\tlength: %d", dev_desc.bLength);
    LOG_HID_DEBUG(L"\tdevice class: %d", dev_desc.bDeviceClass);
    LOG_HID_DEBUG(L"\tS/N: %d", dev_desc.iSerialNumber);
    LOG_HID_DEBUG(L"\tVID:PID: %04X:%04X", dev_desc.idVendor, dev_desc.idProduct);
    LOG_HID_DEBUG(L"\tbcdDevice: %04X", dev_desc.bcdDevice);
    LOG_HID_DEBUG(L"\tiMan:iProd:iSer: %d:%d:%d", dev_desc.iManufacturer, dev_desc.iProduct, dev_desc.iSerialNumber);
    LOG_HID_DEBUG(L"\tnb confs: %d", dev_desc.bNumConfigurations);
  }
  // 读取配置描述 Reading configuration descriptor
  struct libusb_config_descriptor *conf_desc;
  if (libusb_get_config_descriptor(dev, 0, &conf_desc) >= 0)
  {
    uint8_t nb_ifaces = conf_desc->bNumInterfaces;
    LOG_HID_DEBUG(L"\tnb interfaces : %d", nb_ifaces);
    LOG_HID_DEBUG(L"\tMaxPower : %d (milliamps)", (conf_desc->MaxPower) * 2);
    uint8_t endpoint_in = 0, endpoint_out = 0;

    for (int i = 0; i < nb_ifaces; i++) {
      LOG_HID_DEBUG(L"\tinterface[%d]: id = %d", i, conf_desc->interface[i].altsetting[0].bInterfaceNumber);
      for (int j = 0; j < conf_desc->interface[i].num_altsetting; j++) {
        LOG_HID_DEBUG(L"\t\tinterface[%d].altsetting[%d]: num endpoints = %d",
          i, j, conf_desc->interface[i].altsetting[j].bNumEndpoints);
        LOG_HID_DEBUG(L"\t\tClass.SubClass.Protocol: %02X.%02X.%02X",
          conf_desc->interface[i].altsetting[j].bInterfaceClass,
          conf_desc->interface[i].altsetting[j].bInterfaceSubClass,
          conf_desc->interface[i].altsetting[j].bInterfaceProtocol);

        if ((conf_desc->interface[i].altsetting[j].bInterfaceClass == LIBUSB_CLASS_MASS_STORAGE)
          && ((conf_desc->interface[i].altsetting[j].bInterfaceSubClass == 0x01)
            || (conf_desc->interface[i].altsetting[j].bInterfaceSubClass == 0x06))
          && (conf_desc->interface[i].altsetting[j].bInterfaceProtocol == 0x50)) {
          // Mass storage devices that can use basic SCSI commands
          test_mode = USE_SCSI;
        }
        for (int k = 0; k < conf_desc->interface[i].altsetting[j].bNumEndpoints; k++) {
          struct libusb_ss_endpoint_companion_descriptor *ep_comp = NULL;
          const struct libusb_endpoint_descriptor *endpoint;
          endpoint = &conf_desc->interface[i].altsetting[j].endpoint[k];
          LOG_HID_DEBUG(L"\t\tendpoint[%d].address: %02X", k, endpoint->bEndpointAddress);

          // Use the first interrupt or bulk IN/OUT endpoints as default for testing
          if ((endpoint->bmAttributes & LIBUSB_TRANSFER_TYPE_MASK) & (LIBUSB_TRANSFER_TYPE_BULK | LIBUSB_TRANSFER_TYPE_INTERRUPT)) {
            if (endpoint->bEndpointAddress & LIBUSB_ENDPOINT_IN) {
              if (!endpoint_in)
                endpoint_in = endpoint->bEndpointAddress;
            }
            else {
              if (!endpoint_out)
                endpoint_out = endpoint->bEndpointAddress;
            }
          }

          if (!((endpoint->bmAttributes & LIBUSB_TRANSFER_TYPE_MASK) ^ (LIBUSB_TRANSFER_TYPE_BULK))) {
            LOG_HID_DEBUG(L"\t\ttransfer type: %s", L"bulk");
          }

          if (!((endpoint->bmAttributes & LIBUSB_TRANSFER_TYPE_MASK) ^ (LIBUSB_TRANSFER_TYPE_INTERRUPT))) {
            LOG_HID_DEBUG(L"\t\ttransfer type: %s", L"interrupt");
          }

          if (!((endpoint->bmAttributes & LIBUSB_TRANSFER_TYPE_MASK) ^ (LIBUSB_TRANSFER_TYPE_ISOCHRONOUS))) {
            LOG_HID_DEBUG(L"\t\ttransfer type: %s", L"isochronous");
          }

          LOG_HID_DEBUG(L"\t\tmax packet size: %04X", endpoint->wMaxPacketSize);
          LOG_HID_DEBUG(L"\t\tpolling interval: %02X", endpoint->bInterval);

          libusb_get_ss_endpoint_companion_descriptor(NULL, endpoint, &ep_comp);
          if (ep_comp) {
            LOG_HID_DEBUG(L"\t\tmax burst: %02X   (USB 3.0)", ep_comp->bMaxBurst);
            LOG_HID_DEBUG(L"\t\t  bytes per interval: %04X (USB 3.0)", ep_comp->wBytesPerInterval);
            libusb_free_ss_endpoint_companion_descriptor(ep_comp);
          }
        }
      }
    }
    // LOG_HID_DEBUG(L"----------------------------------------------");
    // for (int iface = 0; iface < nb_ifaces; iface++)
    // {
    //   LOG_HID_DEBUG(L"Claiming interface %d...", iface);
    //   int r = libusb_claim_interface(m_devHandle, iface);
    //   if (r != LIBUSB_SUCCESS) {
    //     LOG_HID_DEBUG(L"libusb_set_auto_detach_kernel_driver Failed.");
    //   }
    // }
  }
  libusb_free_config_descriptor(conf_desc);
  libusb_set_auto_detach_kernel_driver(m_devHandle, 1);
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
