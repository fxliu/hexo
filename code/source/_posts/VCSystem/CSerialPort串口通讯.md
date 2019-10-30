---
title: 串口通讯
tags: 
  - 串口
  - 通讯
categories: 
  - VC
description: 串口
date: 2019-10-27 ‏‎15:35:33
updated: 2019-10-27 ‏‎15:35:33
---

## API

+ `CreateFile`: 打开串口，文件名指定为`COM2`即可
+ 参数设置：
  + `SetCommTimeouts`: 读写超时控制
  + `SetCommState`: 设置参数
    + `GetCommState`: 获取参数(DCB)
    + 先获取，调整需要修改的项，然后再设置
    + 注意停止位的定义：0代表1个停止位，1代表1.5个停止位，2代表2个停止位

```C++
// 常用字段
typedef struct _DCB {
    DWORD DCBlength;      /* sizeof(DCB)                     */
    DWORD BaudRate;       /* 波特率：115200,9600等       */
    DWORD fBinary: 1;     /* 数据位：通常为8    */
    DWORD fParity: 1;     /* 奇偶检验位          */
    BYTE StopBits;        /* 停止位：0,1,2 = 1, 1.5, 2        */
} DCB, *LPDCB;
```

+ `PurgeComm`: 清空缓冲区
  + PURGE_TXABORT：中断所有写操作并立即返回，即使写操作还没有完成。
  + PURGE_RXABORT：中断所有读操作并立即返回，即使读操作还没有完成。
  + PURGE_TXCLEAR：清除输出缓冲区
  + PURGE_RXCLEAR：清除输入缓冲区
+ `ReadFile`: 读
+ `WriteFile`: 写
+ 串口遍历
  + `SetupDiGetClassDevs`: 打开句柄
    + GUID: `GUID_CLASS_COMPORT`，在`WinIoCtl.h`文件中被定义
    + `SetupDiDestroyDeviceInfoList`：释放句柄
  + `SetupDiEnumDeviceInterfaces`: 遍历
  + `SetupDiGetDeviceInterfaceDetail`: 接口路径，比如“COM2”什么的
  + `SetupDiGetDeviceRegistryProperty`：接口属性
    + `SPDRP_DEVICEDESC`：设备描述
    + `SPDRP_CLASS`：类名
    + `SPDRP_MFG`：制造商
    + `SPDRP_FRIENDLYNAME`：设备描述(友好名称)
    + `SPDRP_LOCATION_INFORMATION`：本地环境属性
    + `SPDRP_PHYSICAL_DEVICE_OBJECT_NAME`：设备物理名称
    + `SPDRP_ENUMERATOR_NAME`：枚举类型

## Demo

[CSerialPort](https://github.com/fxliu/VCDemo/tree/master/SYSTEM/CSerialPort)

## GitHub第三方库

+ [CSerialPort](https://github.com/itas109/CSerialPort)，支持Windows/Linux，封装比较完善
+ 直接搜索`CSerialPort`也有其他一些简单封装
