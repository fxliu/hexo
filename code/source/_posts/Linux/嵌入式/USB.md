---
title: USB
tags: 
  - USB
categories: 
  - 嵌入式
description: USB
date: 2023-04-07 16:12:33
updated: 2023-04-07 16:12:33
---

## 组合设备
> USB复合设备: Compound Device内嵌Hub和多个Function，每个Function都相当于一个独立的USB外设，有自己的PID/VID
> USB组合设备: Composite Device内只有一个Function，只有一套PID/VID，通过将不同的interface定义为不同的类来实现多个功能的组合


> USB复合设备一般用Interface Association Descriptor（IAD）实现，就是在要合并的接口前加上IAD描述符
> 在配置描述符中, 添加IAD描述即可

* bLength: 描述符大小, 固定值0x08
* bDescriptorType: IAD描述符类型, 固定值0x0B
* bFirstInterface: 起始接口
* bInterfaceCount: 接口数
* bFunctionClass: 类型代码
* bFunctionSubClass: 子类型代码
* bFunctionProtocol: 协议代码
* iFunction: 描述字符串索引

```c++
  /* Interface Association Descriptor(IAD Descriptor)  */ 
	0x08,      /*   bLength  */
	0x0B,      /*   bDescriptorType*/
	0x00,      /*   bFirstInterface*/
	0x02,      /*   bInterfaceCount*/
	0x02,      /*   bFunctionClass --CDC*/
	0x02,      /*   bFunctionSubClass*/
	0x01,      /*   bFunctionProtocoll*/
	0x00,      /*   iFunction */
```

## 设备描述符

| 偏移量 | 字段名称           | 长度(字节) | 字段值 | 意义                       |
| ------ | ------------------ | ---------- | ------ | -------------------------- |
| 0      | bLength            | 1          | 数字   | 设备描述符的字节数大小     |
| 1      | bDescriptorType    | 1          | 常数   | 设备描述符类型编号         |
| 2      | bcdUSB             | 2          | BCD码  | USB版本号                  |
| 4      | bDeviceClass       | 1          | 类     | USB分配的设备类代码        |
| 5      | bDeviceSubClass    | 1          | 子类   | USB分配的子类代码          |
| 6      | bDeviceProtocol    | 1          | 协议   | USB分配的设备协议代码      |
| 7      | BMaxPacketSize    | 1          | 数字   | 端点0的最大包大小          |
| 8      | idVendor           | 2          | ID编号 | 厂商编号                   |
| 10     | idProduct          | 2          | ID编号 | 产品编号                   |
| 12     | bcdDevice          | 2          | BCD码  | 设备出厂编号               |
| 14     | iManufacturer      | 1          | 索引   | 描述厂商字符串的索引       |
| 15     | iProduct           | 1          | 索引   | 描述产品字符串的索引       |
| 16     | iSerialNumber      | 1          | 索引   | 描述设备序列号字符串的索引 |
| 17     | bNumConfigurations | 1          | 数字   | 可能的配置参数             |

> bLength: 整个设备描述符占用了17个字节, 因此bLength是固定值(0x12)
> bDescriptorType: 设备描述符的类型，USB定义的设备描述符的类型编号为固定值0x01
> BCD码: USB版本号: USB1.1(0x0110), USB2.0(0x0200)
> bDeviceClass: 设备类型的代码，值从0x01~0xFE为USB定义的标准设备类，而值为0xFF时表示该设备类型代码是厂商自定义的类。如果设备类型不是在设备描述符中定义的, 则该值为0, 比如人机接口设备 ( HID) 类。
> bDEviceSubClass: 设备类中的子类类型，和bDeviceClass一样由USB规定和分配，当 bDeviceClass为0时, 此值也为0, 代表该子类类型不在设备描述符中定义。 值为0xFF时, 也代表子类类型是由厂商所定义的。
> bDeviceProtocol: 设备所遵循的协议，该值有USB协议规定，当值为0xFF时，表示该设备采用厂商自己为该类定义的协议
> bMaxPacketSize: 描述了端点0的最大包的大小, 低速设备的bMaxPacketSize0恒为8, 全速设备可以是0x08、0x10、0x20或0x40, 而高速设备则为64
> idVendor: USB设备的生产厂商从USB开发者论坛(USB Implementers Forum)获得的ID号
> idProduct: 设备的生产厂商所定义的该设备的产品ID号
> bcdDevice: 设备生产厂商来定义, 代表该设备的产品版本号
> iMenufacturer: 设备生产厂商的字符串的索引值。值为0则代表没有使用该字段
> iProduct: 描述该产品的字符串的索引值。值为0时表示没有使用该字段
> iSerialNumber: 设备的序列号的索引值。每个设备都有一个特定的序列号, 可供主机来识别不同的设备
> bNumConfigurations: 该设备总共支持的配置描述符的数量

## 设备限定描述符
> 设备限定描述符(Device Qualifier Descriptor)说明了能进行高速操作的设备在其他速度时产生的变化信息。
> 如果设备既支持全速状态又支持高速状态，那么就必须含有设备限定描述符(Device Qualifier Descriptor)。
> 这个描述符的版本号至少是2.0(0200H)

```c++
// 字段和[设备描述符]基本是一致的
#define  USB_LEN_DEV_QUALIFIER_DESC                     0x0A
__ALIGN_BEGIN uint8_t USBD_DeviceQualifierDesc[USB_LEN_DEV_QUALIFIER_DESC] __ALIGN_END =
{
  USB_LEN_DEV_QUALIFIER_DESC,   // bLength: 固定值
  0x06,                         // bDescriptorType: 固定值
  0x00,                       /*bcdUSB: USB2.0 */
  0x02,

  0x02,                       /*bDeviceClass: 串口*/
  0x00,                       /*bDeviceSubClass*/
  0x00,                       /*bDeviceProtocol*/

  0x40,                       /*bMaxPacketSize*/

  0x01,                       // bNumConfigurations: 其他速度配置的数量
  0x00,                       // 保留
};
```

## 描述符: Configuration Descriptor

### 配置描述符
> 配置描述符用于描述一个USB设备的属性和能力等配置信息。一个USB设备只需要一个配置描述符就可以了。

* bLength: 整个配置描述符的长度, 固定值0x09
* bDescriptorType: USB给配置描述符分配的类型编号, 值为常数0x02
* wTotalLength: 所有描述符(包括配置、接口和端点描述符)的大小总和
* bNumInterfaces: 该字段的值作为参数, 可被Set_Configuration和 Get_Configuration命令来调用, 用于该命令选定这个配置
* iConfiguration: 该字段指向描述该配置描述符的字符串。 如果该设备没有用字符串描述该配置, 那么此字段为0
* bmAttributes: 该字段1字节二进制数的每一位代表一个固定的含义
  * D7：Reserve，固定为1
  * D6：供电方式的选择, 值为1表示自供电, 值为0表示总线供电
  * D5：远程唤醒功能的选择, 值为1表示支持远程唤醒, 值为0则不支持
  * D4~D0：没有意义, 均把值固定为0
* MaxPower: 设备从总线上获取的电流总量。电流值为字段值的两倍，设备可以获取到的最大电流为500mA,所以字段值最大为0xFA

```c++
// 组合设备
  0xEF,                       /*bDeviceClass*/
  0x02,                       /*bDeviceSubClass*/
  0x01,                       /*bDeviceProtocol*/
```

### 接口描述符
> 接口一般是由一系列端点所组成的集合体,用于实现某种特定的USB的数据传输功能

* bLength: 接口描述符的长度，固定为0x09
* bDescriptorType: 由USB给配置描述符分配的类型编号, 值为常数0x04
* bInterfaceNumber: 接口的编号，每一个接口都有惟一的编号, USB就是通过此字段来识别不同的接口。默认值为0
* bAlternateSetting: 
* bNumEndpoints: 该接口使用的端点总数, 如果此值为0, 则意味着该接口只使用了端点0
* bInterfaceClass: 该接口所属的类别。这个类别编号由USB来分配。当值为0xFF时, 表示该接口是厂商所定义的接口类型。而值0保留。
* bInterfaceSubClass: 接口所属的类别中的子类类型。这个子类编号也由USB分配。同bInterfaceClass字段一样, 当其值为0xFF时代表该接口由厂商自己所定义。而值0保留。
* bInterfaceProtocol: 此接口类所遵循的类的协议。因而, 该字段的值跟bInterfaceClass和bInterfaceSubClass字段是相关的。其值从1～0xFE由USB分配, 代表不同标准的设备类的协议。 当值为0时, 表示该接口不遵循任何类协议; 而值为0xFF时, 表示该接口应用了厂商自定义的类协议。
iInterface: 指向字符串描述符中相应的字符串内容, 用于描述该接口。 如果设备没有启用字符串描述符 , 则该值为0

### 端点描述符
> 端点描述符用于描述接口所使用的非0端点的属性, 包括输入/输出方向、端点号和端点容量即包的大小等。

* bLength: 端点描述符的长度
* bDescriptorType: USB为端点描述符分配的类型编号, 此字段的值固定(0x05)
* bEndpointAddress: 
  * D7 端点方向, 0 OUT, 1 IN
  * D6～D4 保留
  * D3～D0 端点编号
* bmAttributes
  * D5~D4: 00 数据端点, 01 反馈端点, 10 隐式反馈数据端点, 11 保留
  * D3~D2: 同步类型, 00 非同步, 01 异步, 10 自适应, 11 同步
  * D1~D0 传输类型, 00 控制传输, 01 同步传输, 10 块传输, 11 中断传输, 如果该端点不是同步端点，D5~D2保留且必须置0
* wMaxPacketSize: 该端点最大包的大小
  * 其中D10～D0位共11位为有效内容。在USB协议1.1中D15～D11位保留, 值为0, 最大包的大小范围为0～1023
* bIterval: 主机轮询设备的周期
  * 在USB协议1.1中, 对于中断端点, 该字段的值为1～255,时间单位ms
  * 对于同步端点, 该字段值固定为1
  * 而批量端点和控制端点则忽略该字段 ,值无效

## 字符串描述符
> 字符串描述符是一个可选的描述符，长度不固定

* bLength: 整个字符串描述符的长度
* bDescriptorType: USB为端点描述符分配的类型编号, 因此, 此字段的值固定, 即为0x03
* bString: 一个以UNICODE编码的字符为内容的字符串

## HID描述符

* bLength: 描述符长度
* bDescriptorType: 描述符类型，HID描述符的类型为0x21
* bcdHID: 所遵循的HID协议版本
* bCountryCode: 国家代码
* bNumDescriptors: 下级描述符数量，通常至少需要一个报告描述符
* bDescriptorType: 下级描述符类型
* wDescriptorLength: 下级描述符长度


## 串口

```c++
#define LOBYTE(x)  ((uint8_t)(x & 0x00FF))
#define HIBYTE(x)  ((uint8_t)((x & 0xFF00) >>8))

#define USB_SIZ_DEVICE_DESC                     0x12
#define USBD_VID                                0x0483
#define USBD_PID                                0x5740
// 设备描述符
__ALIGN_BEGIN uint8_t USBD_DeviceDesc[USB_SIZ_DEVICE_DESC] __ALIGN_END =
{
  0x12,                       /*bLength*/
  0x01,                       /*bDescriptorType: USB*/
  0x00,                       /*bcdUSB: USB2.0 */
  0x02,

  0x02,                       /*bDeviceClass: CDC*/
  0x00,                       /*bDeviceSubClass*/
  0x00,                       /*bDeviceProtocol*/

  0x40,                       /*bMaxPacketSize*/
  LOBYTE(USBD_VID),           /*idVendor*/
  HIBYTE(USBD_VID),           /*idVendor*/
  LOBYTE(USBD_PID),           /*idVendor*/
  HIBYTE(USBD_PID),           /*idVendor*/

  0x00,                       /*bcdDevice rel. 1.00*/
  0x01,

  0x01,                       /*Index of manufacturer  string*/
  0x02,                       /*Index of product string*/
  0x03,                       /*Index of serial number string*/
  0x01                        /*bNumConfigurations*/
} ; /* USB_DeviceDescriptor */

#define USB_CDC_CONFIG_DESC_SIZ         0x43  // 67
#define CDC_IN_EP                       0x81  /* EP1 for data IN */
#define CDC_OUT_EP                      0x01  /* EP1 for data OUT */
#define CDC_CMD_EP                      0x82  /* EP2 for CDC commands */
#define CDC_DATA_MAX_PACKET_SIZE        0x40  /* Endpoint IN & OUT Packet size */
#define CDC_CMD_PACKET_SZE              0x08  /* Control Endpoint Packet size */
// 配置描述符
__ALIGN_BEGIN uint8_t usbd_cdc_CfgDesc[USB_CDC_CONFIG_DESC_SIZ]  __ALIGN_END =
{
    /*Configuration Descriptor: 配置描述符*/
    0x09,   /* bLength: Configuration Descriptor size */
    0x02,   /* bDescriptorType: Configuration */
    USB_CDC_CONFIG_DESC_SIZ,  /* wTotalLength: no of returned bytes */
    0x00,                     /* wTotalLength */
    0x02,   /* bNumInterfaces: 2 interface */
    0x01,   /* bConfigurationValue: Configuration value */
    0x00,   /* iConfiguration: Index of string descriptor describing the configuration */
    0xC0,   /* bmAttributes: self powered */
    0x32,   /* MaxPower 0 mA */
    /*---------------------------------------------------------------------------*/
    /*Interface Descriptor: 管控接口*/
    0x09,   /* bLength: Interface Descriptor size */
    0x04,  /* bDescriptorType: Interface */
    /* Interface descriptor type */
    0x00,   /* bInterfaceNumber: Number of Interface */
    0x00,   /* bAlternateSetting: Alternate setting */
    0x01,   /* bNumEndpoints: One endpoints used */
    0x02,   /* bInterfaceClass: Communication Interface Class */
    0x02,   /* bInterfaceSubClass: Abstract Control Model */
    0x01,   /* bInterfaceProtocol: Common AT commands */
    0x00,   /* iInterface: Index of string descriptor*/

    /*Header Functional Descriptor*/
    0x05,   /* bLength: Endpoint Descriptor size */
    0x24,   /* bDescriptorType: CS_INTERFACE */
    0x00,   /* bDescriptorSubtype: Header Func Desc */
    0x10,   /* bcdCDC: spec release number */
    0x01,

    /*Call Management Functional Descriptor*/
    0x05,   /* bFunctionLength */
    0x24,   /* bDescriptorType: CS_INTERFACE */
    0x01,   /* bDescriptorSubtype: Call Management Func Desc */
    0x00,   /* bmCapabilities: D0+D1 */
    0x00,   /* bDataInterface: 0 */

    /*ACM Functional Descriptor*/
    0x04,   /* bFunctionLength */
    0x24,   /* bDescriptorType: CS_INTERFACE */
    0x02,   /* bDescriptorSubtype: Abstract Control Management desc */
    0x02,   /* bmCapabilities */

    /*Union Functional Descriptor*/
    0x05,   /* bFunctionLength */
    0x24,   /* bDescriptorType: CS_INTERFACE */
    0x06,   /* bDescriptorSubtype: Union func desc */
    0x00,   /* bMasterInterface: Communication class interface */
    0x01,   /* bSlaveInterface0: Data Class Interface */

    /*Endpoint 2 Descriptor*/
    0x07,                           /* bLength: Endpoint Descriptor size */
    0x05,                           /* bDescriptorType: Endpoint */
    CDC_CMD_EP,                     /* bEndpointAddress */
    0x03,                           /* bmAttributes: Interrupt */
    LOBYTE(CDC_CMD_PACKET_SZE),     /* wMaxPacketSize: */
    HIBYTE(CDC_CMD_PACKET_SZE),
#ifdef USE_USB_OTG_HS
    0x10,                           /* bInterval: */
#else
    0xFF,                           /* bInterval: */
#endif /* USE_USB_OTG_HS */

    /*---------------------------------------------------------------------------*/
    /*Data class interface descriptor: 数据接口*/
    0x09,   /* bLength: Endpoint Descriptor size */
    0x04,   /* bDescriptorType: */
    0x01,   /* bInterfaceNumber: Number of Interface */
    0x00,   /* bAlternateSetting: Alternate setting */
    0x02,   /* bNumEndpoints: Two endpoints used */
    0x0A,   /* bInterfaceClass: CDC */
    0x00,   /* bInterfaceSubClass: */
    0x00,   /* bInterfaceProtocol: */
    0x00,   /* iInterface: */

    /*Endpoint OUT Descriptor*/
    0x07,                              /* bLength: Endpoint Descriptor size */
    0x05,                              /* bDescriptorType: Endpoint */
    CDC_OUT_EP,                        /* bEndpointAddress */
    0x02,                              /* bmAttributes: Bulk */
    LOBYTE(CDC_DATA_MAX_PACKET_SIZE),  /* wMaxPacketSize: */
    HIBYTE(CDC_DATA_MAX_PACKET_SIZE),
    0x00,                              /* bInterval: ignore for Bulk transfer */

    /*Endpoint IN Descriptor*/
    0x07,                              /* bLength: Endpoint Descriptor size */
    0x05,                              /* bDescriptorType: Endpoint */
    CDC_IN_EP,                         /* bEndpointAddress */
    0x02,                              /* bmAttributes: Bulk */
    LOBYTE(CDC_DATA_MAX_PACKET_SIZE),  /* wMaxPacketSize: */
    HIBYTE(CDC_DATA_MAX_PACKET_SIZE),
    0x00                               /* bInterval: ignore for Bulk transfer */
} ;

```

## SDT
> 只有数据接口的串口

```c++
#define USB_SIZ_DEVICE_DESC                     0x12
// 设备描述符
__ALIGN_BEGIN uint8_t USBD_DeviceDesc[USB_SIZ_DEVICE_DESC] __ALIGN_END =
{
  0x12,                       //bLength
  0x01,                       //bDescriptorType: USB
  0x00,                       //bcdUSB: USB2.0
  0x02,

  0x02,                       //bDeviceClass: 串口
  0x00,                       //bDeviceSubClass
  0x00,                       //bDeviceProtocol

  0x40,                       //bMaxPacketSize
  0x00,                       //idVendor:  固定值
  0x04,                       //idVendor:  固定值
  0x5A,                       //idProduct: 固定值
  0xC3,                       //idProduct: 固定值

  0x00,                       //bcdDevice rel. 2.00
  0x02,  
  
  0x03,                       //Index of manufacturer  string
  0x02,                       //Index of product string
  0x01,                       //Index of serial number string
  0x01                        //bNumConfigurations
} ; /* USB_DeviceDescriptor */

#define CDC_IN_EP                       0x81  /* EP1 for data IN */
#define CDC_OUT_EP                      0x02  /* EP1 for data OUT */
#define CDC_CMD_EP                      0x82  /* EP2 for CDC commands */
#define USB_CDC_CONFIG_DESC_SIZ         0x20  // 32
#define CDC_DATA_MAX_PACKET_SIZE        0x40  /* Endpoint IN & OUT Packet size */
// 配置描述符
/* USB CDC device Configuration Descriptor */
__ALIGN_BEGIN uint8_t usbd_cdc_CfgDesc[USB_CDC_CONFIG_DESC_SIZ]  __ALIGN_END =
{
  /*Configuration Descriptor*/
  0x09,   /* bLength: Configuration Descriptor size */
  0x02,   /* bDescriptorType: Configuration */
  USB_CDC_CONFIG_DESC_SIZ,                /* wTotalLength:no of returned bytes */
  0x00,
  0x01,   /* bNumInterfaces: 2 interface */
  0x01,   /* bConfigurationValue: Configuration value */
  0x00,   /* iConfiguration: Index of string descriptor describing the configuration */
  0xC0,   /* bmAttributes: self powered */
  0x32,   /* MaxPower 0 mA */
  
  /*---------------------------------------------------------------------------*/
  /*Interface Descriptor */
  0x09,   /* bLength: Interface Descriptor size */
  0x04,   /* bDescriptorType: Interface */
  /* Interface descriptor type */
  0x01,   /* bInterfaceNumber: Number of Interface */
  0x00,   /* bAlternateSetting: Alternate setting */
  0x02,   /* bNumEndpoints: One endpoints used */
  0x0A,   /* bInterfaceClass: Communication Interface Class, CDC */
  0x00,   /* bInterfaceSubClass: Abstract Control Model */
  0x00,   /* bInterfaceProtocol: Common AT commands */
  0x00,   /* iInterface: */
  
  /*Endpoint OUT Descriptor*/
  0x07,   /* bLength: Endpoint Descriptor size */
  0x05,   /* bDescriptorType: Endpoint */
  CDC_IN_EP,                         /* bEndpointAddress */
  0x02,                              /* bmAttributes: Bulk */
  LOBYTE(CDC_DATA_MAX_PACKET_SIZE),  /* wMaxPacketSize: */
  HIBYTE(CDC_DATA_MAX_PACKET_SIZE),
  0x00,                              /* bInterval: ignore for Bulk transfer */
  
  /*Endpoint IN Descriptor*/
  0x07,   /* bLength: Endpoint Descriptor size */
  0x05,   /* bDescriptorType: Endpoint */
  CDC_OUT_EP,                        /* bEndpointAddress */
  0x02,                              /* bmAttributes: Bulk */
  LOBYTE(CDC_DATA_MAX_PACKET_SIZE),  /* wMaxPacketSize: */
  HIBYTE(CDC_DATA_MAX_PACKET_SIZE),
  0x00                               /* bInterval: ignore for Bulk transfer */
} ;
```

## HID

```c++
#define USB_SIZ_DEVICE_DESC                     0x12
// 设备描述符
__ALIGN_BEGIN uint8_t USBD_DeviceDesc[USB_SIZ_DEVICE_DESC] __ALIGN_END =
{
  0x12,           //bLength
  0x01,           //bDescriptorType: USB
  0x02, 0x00,     //bcdUSB: USB2.0

  0x00,           //bDeviceClass: HID
  0x00,           //bDeviceSubClass
  0x00,           //bDeviceProtocol

  0x40,           //bMaxPacketSize
  0x83, 0x04,     //idVendor
  0x06, 0xE8,     //idProduct

  0x00,           //bcdDevice rel. 2.00
  0x02,

  0x01,           //iManufacturer
  0x02,           //iProduct
  0x03,           //iSerialNumber
  0x01            //bNumConfigurations
} ; /* USB_DeviceDescriptor */

#define HID_REPORT_DESC_SIZE          0x22  // 44
#define USB_HID_CONFIG_DESC_SIZ       0x29  // 41
// 配置描述符
__ALIGN_BEGIN uint8_t USBD_HID_CfgDesc[USB_HID_CONFIG_DESC_SIZ] __ALIGN_END =
{
  //configuration desc
  0x09,                                 //Length = 9
  0x02,                                 //DescriptorType, USB
  USB_HID_CONFIG_DESC_SIZ, 0x00,        //TotalLength
  0x01,                                 //NumInterfaces = 1
  0x01,                                 //ConfigurationValue = 1
  0x00,                                 //iConfiguration string index(Non)
  0x80,                                 //SelfPower = 0; RemoteWakeup = 0
  0x32,                                 //MaxPower = 100mA

  //interface desc                      
  0x09,                                 //Length = 9
  0x04,                                 //DescriptorType = Interface
  0x00,                                 //InerfaceNumber = 0
  0x00,                                 //AlternateSetting = 0
  0x02,                                 //NumEndpoint = 2(bulk-IN, bulk-OUT)
  0x03,                                 //Class = Human Interface Device 
  0x00,                                 //InterfaceSubClass = 0x00(No subclass)     
  0x00,                                 //InterfaceProtocol = 0x00(None) 
  0x00,                                 //iInterface string index(Non)
  
  //HID descriptor
  0x09,0x21,                            //Length, Type
  0x10,0x01,                            //HID Class Specification compliance ?0x10 0x01
  0x00,                                 //Country localization (=none)
  0x01,                                 //number of descriptors to follow
  0x22,                                 //And it's a Report descriptor
  HID_REPORT_DESC_SIZE,0x00,            //Report descriptor length - 报告描述符长度

  // Endpoint desc
  0x07,                                 //Length = 7
  0x05,                                 //DescriptorType = Endpoint
  0x81,                                 //In; Ep1
  0x03,                                 //Endpoint type = interrupt
  0x40, 0x00,                           //MaxPacketSize = 64
  0x01,                                 //Poll

  0x07,                                 //Length = 7
  0x05,                                 //DescriptorType = Endpoint
  0x02,                                 //Out; Ep2
  0x03,                                 //Endpoint type = interrupt
  0x40, 0x00,                           //MaxPacketSize = 64
  0x01,                                 //Interval(ignore)
};
// HID - 报告描述符
__ALIGN_BEGIN uint8_t HID_ReportDesc[HID_REPORT_DESC_SIZE] __ALIGN_END =
{
  0x06, 0x00, 0xFF,  //Usage Page:
  0x09, 0x01,   //Usage: Undefined
  0xa1, 0x01,   //Collection

  0x09, 0x03,  //Usage (vendor-defined)
  0x15, 0x00,  //Logical Minimum
  0x25, 0xFF,  //Logical Maximum
  0x95, 0x40,  //Feature_Length, //Report Count
  0x75, 0x08,  //Report Size 
  0x81, 0x02,  //Input (Data, Variable, Absolute,Buffered Bytes)

  0x09, 0x04,  //Usage (vendor-defined)
  0x15, 0x00,  //Logical Minimum
  0x25, 0xFF,  //Logical Maximum
  0x95, 0x40,  //Feature_Length, //Report Count
  0x75, 0x08,  //Report Size 
  0x91, 0x02,  //Output (Data, Variable, Absolute,Buffered Bytes)

  0x09, 0x05,  //Usage (vendor-defined)
  0x15, 0x00,  //Logical Minimum
  0x25, 0xFF,  //Logical Maximum
  0x95, 0x40,  //Feature_Length, //Report Count
  0x75, 0x08,  //Report Size 
  0xb1, 0x02,  //Feature (Data, Variable, Absolute,Buffered Bytes)
  0xc0   //End Collection
};
```

## USB键盘

```c++
#define USB_HID_CONFIG_DESC_SIZ       0x29  // 44
#define HID_KEY_REPORT_DESC_SIZE      0x3F  // 63
// 配置描述符
__ALIGN_BEGIN uint8_t USBD_HID_CfgDesc[USB_HID_CONFIG_DESC_SIZ] __ALIGN_END =
{
  //configuration desc
  0x09,                                 //Length = 9
  0x02,                                 //DescriptorType = Configuration
  USB_HID_CONFIG_DESC_SIZ, 0x00,        //TotalLength = (9 for Configuration; 9 for Interface; 54 for CCID; 7 for Bulk-in, 7 for Bulk-Out Endpoint)
  0x01,                                 //NumInterfaces = 1
  0x01,                                 //ConfigurationValue = 1
  0x00,                                 //iConfiguration string index(Non)
  0x80,                                 //SelfPower = 0; RemoteWakeup = 0
  0x32,                                 //MaxPower = 100mA
                                        
  //interface desc                      
  0x09,                                 //Length = 9
  0x04,                                 //DescriptorType = Interface
  0x00,                                 //InerfaceNumber = 0
  0x00,                                 //AlternateSetting = 0
  0x02,                                 //NumEndpoint = 2(bulk-IN, bulk-OUT)
  0x03,                                 //Class = Human Interface Device 
  0x01,                                 //InterfaceSubClass = 0x00(No subclass)     
  0x01,                                 //InterfaceProtocol = 0x00(None) 
  0x00,                                 //iInterface string index(Non)
  
  //HID descriptor
  0x09,0x21,                            //Length, Type
  0x00,0x01,                            //HID Class Specification compliance ?0x10 0x01
  0x00,                                 //Country localization (=none)
  0x01,                                 //number of descriptors to follow
  0x22,                                 //And it's a Report descriptor
  HID_KEY_REPORT_DESC_SIZE,0x00,        //Report descriptor length 

  // Endpoint desc
  0x07,                                 //Length = 7
  0x05,                                 //DescriptorType = Endpoint    
  0x81,                                 //In; Ep1
  0x03,                                 //Endpoint type = interrupt
  0x08, 0x00,                           //MaxPacketSize = 64
  0x01,                                 //Poll

  0x07,                                 //Length = 7
  0x05,                                 //DescriptorType = Endpoint    
  0x01,                                 //Out; Ep2
  0x03,                                 //Endpoint type = interrupt
  0x08, 0x00,                           //MaxPacketSize = 64
  0x01,                                 //Interval(ignore)
} ;

// HID - 报告描述符 - USB键盘
__ALIGN_BEGIN uint8_t HID_MOUSE_ReportDesc[HID_MOUSE_REPORT_DESC_SIZE] __ALIGN_END =
{
  0x05, 0x01, // USAGE_PAGE (Generic Desktop)         //表示用途页为通用桌面设备
  0x09, 0x06, // USAGE (Keyboard)                     //表示用途为键盘
  0xa1, 0x01, // COLLECTION (Application)             //表示应用集合，必须要以END_COLLECTION来结束它，见最后的END_COLLECTION
  
  0x05, 0x07, // USAGE_PAGE (Keyboard)                //表示用途页为按键
  0x19, 0xe0, // USAGE_MINIMUM (Keyboard LeftControl) //用途最小值，这里为左ctrl键
  0x29, 0xe7, // USAGE_MAXIMUM (Keyboard Right GUI)   //用途最大值，这里为右GUI键，即window键
  0x15, 0x00, // LOGICAL_MINIMUM (0)                  //逻辑最小值为0
  0x25, 0x01, // LOGICAL_MAXIMUM (1)                  //逻辑最大值为1
  
  0x95, 0x08, // REPORT_COUNT (8)                     //报告的个数为8，即总共有8个bits
  0x75, 0x01, // REPORT_SIZE (1)                      //报告大小（即这个字段的宽度）为1bit，所以前面的逻辑最小值为0，逻辑最大值为1
  //输入用，变量，值，绝对值。像键盘这类一般报告绝对值，
  //而鼠标移动这样的则报告相对值，表示鼠标移动多少
  0x81, 0x02, // INPUT (Data,Var,Abs)
  //上面这这几项描述了一个输入用的字段，总共为8个bits，每个bit表示一个按键
  //分别从左ctrl键到右GUI键。这8个bits刚好构成一个字节，它位于报告的第一个字节。
  //它的最低位，即bit-0对应着左ctrl键，如果返回的数据该位为1，则表示左ctrl键被按下，
  //否则，左ctrl键没有按下。最高位，即bit-7表示右GUI键的按下情况。中间的几个位，
  //需要根据HID协议中规定的用途页表（HID Usage Tables）来确定。这里通常用来表示
  //特殊键，例如ctrl，shift，del键等

  0x95, 0x01, // REPORT_COUNT (1)                     //这样的数据段个数为1
  0x75, 0x08, // REPORT_SIZE (8)                      //每个段长度为8bits
  0x81, 0x03, // INPUT (Cnst,Var,Abs)                 //输入用，常量，值，绝对值
  //上面这8个bit是常量，设备必须返回0

  0x95, 0x05, // REPORT_COUNT (5)                     //这样的数据段个数为5
  0x75, 0x01, // REPORT_SIZE (1)                      //每个段大小为1bit
  0x05, 0x08, // USAGE_PAGE (LEDs)                    //用途是LED，即用来控制键盘上的LED用的，因此下面会说明它是输出用
  0x19, 0x01, // USAGE_MINIMUM (Num Lock)             //用途最小值是Num Lock，即数字键锁定灯
  0x29, 0x05, // USAGE_MAXIMUM (Kana)                 //用途最大值是Kana，这个是什么灯我也不清楚^_^
  0x91, 0x02, // OUTPUT (Data,Var,Abs)                //1表示灯亮，0表示灯灭
  //如前面所说，这个字段是输出用的，用来控制LED。变量，值，绝对值。

  0x95, 0x01, // REPORT_COUNT (1)                     //这样的数据段个数为1
  0x75, 0x03, // REPORT_SIZE (3)                      //每个段大小为3bits
  0x91, 0x03, // OUTPUT (Cnst,Var,Abs)
  //由于要按字节对齐，而前面控制LED的只用了5个bit，
  //所以后面需要附加3个不用bit，设置为常量。

  0x95, 0x06, // REPORT_COUNT (6)                     //报告个数为6
  0x75, 0x08, // REPORT_SIZE (8)                      //每个段大小为8bits
  0x15, 0x00, // LOGICAL_MINIMUM (0)                  //逻辑最小值0
  0x25, 0xFF, // LOGICAL_MAXIMUM (255)                //逻辑最大值255
  0x05, 0x07, // USAGE_PAGE (Keyboard)                //用途页为按键
  0x19, 0x00, // USAGE_MINIMUM (Reserved (no event indicated))  //使用最小值为0
  0x29, 0x65, // USAGE_MAXIMUM (Keyboard Application) //使用最大值为0x65
  0x81, 0x00, // INPUT (Data,Ary,Abs)                 //输入用，变量，数组，绝对值
  //以上定义了6个8bit宽的数组，每个8bit（即一个字节）用来表示一个按键，所以可以同时
  //有6个按键按下。没有按键按下时，全部返回0。如果按下的键太多，导致键盘扫描系统
  //无法区分按键时，则全部返回0x01，即6个0x01。如果有一个键按下，则这6个字节中的第一
  //个字节为相应的键值（具体的值参看HID Usage Tables），如果两个键按下，则第1、2两个
  //字节分别为相应的键值，以次类推。
  //关集合，跟上面的对应
  0xc0 // END_COLLECTION
};
// 每次事件发送一个8B的数组
// 按键和弹起都要发送事件, 数组中包含指定按键描述认为按下, 下次事件无该按键描述认为弹起
// 1B: 标示功能键, 每一个bit标示一个功能键是否被按下
#define KEY_L_CTRL   0x01
#define KEY_L_SHIFT  0x02
#define KEY_L_ALT    0x04
#define KEY_L_WIN    0x08
#define KEY_R_CTRL   0x10
#define KEY_R_SHIFT  0x20
#define KEY_R_ALT    0x40
#define KEY_R_WIN    0x80
// 1B: 灯语, 前5bit有效, 后3bit对齐用
// 6B: 按键, 最多描述6个按键被按下
// 按键值对应
u8* KeyMap(u8 n, u8* data) {
  u8 keymap[37]={
    0x27,0x1E,0x1F,0x20,0x21,0x22,0x23,0x24,0x25,0x26, //0-9
    0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x10,0x11,
    0x12,0x13,0x14,0x15,0x16,0x17,0x018,0x19,0x1A,0x1B,0x1C,0x1D
  };
  if('0'<= n && n<='9'){
    data[2] = keymap[n-'0'];
    data[0] = 0;
  }
  else if('a'<=n && n<='z'){
    data[2] = keymap[n-'a'+10];
    data[0] = 0;
  }
  else if('A'<=n && n<='Z'){
    // LeftShift
    data[2] = keymap[n-'A'+10];
    data[0] = KEY_L_SHIFT;
  }
  else if('\n' == n) {
    data[2] = 0x28;
    data[0] = 0;
  }
  else {
    data[0] = 0;
    data[2] = 0;
  }
  return data;
}
```
