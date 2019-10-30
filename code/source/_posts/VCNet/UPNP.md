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

## UPNP

用即插即用（英语：Universal Plug and Play，简称UPnP）是由“通用即插即用论坛”（UPnP™ Forum）推广的一套网络协议。
该协议的目标是使家庭网络（数据共享、通信和娱乐）和公司网络中的各种设备能够相互无缝连接，并简化相关网络的实现。
UPnP通过定义和发布基于开放、因特网通讯网协议标准的UPnP设备控制协议来实现这一目标。
UPnP这个概念是从即插即用（Plug-and-play）派生而来的，即插即用是一种热拔插技术。

## UPNP穿透(WIN API)

NAT穿透允许UPnP数据包在没有用户交互的情况下，无障碍的通过路由器或者防火墙（假如那个路由器或者防火墙支持NAT）。
事实上大部分防火墙默认都是开通这个端口的

### 初始化COM接口

```CoInitialize(NULL)```

```C++
typedef enum _EPortMapping
{
  PM_OK = 0,				// 操作成功
  PM_SUCCESS = 0,			// 未注册 && 可注册
  PM_SUCCESS_EXIST,		// 已注册
  PM_ERROR = 10,			// 操作失败
  PM_ERROR_PORT,			// 外网端口已被本机其他端口映射
  PM_ERROR_REMOTE_PORT,	// 外网端口已被其他机器映射
  PM_ERROR_PORT_CONFLICT,	// 端口冲突：端口必须 >= 1024
}EPortMapping;

// 定义结构体模型：每个IUPnPDevice都有子IUPnPDevice组以及自身提供的IUPnPService组
typedef struct _MyUpnpService
{
public:
  CComVariant cv;
  CComPtr<IUPnPService> service;
  _MyUpnpService(CComVariant &cv)
  {
    this->cv = cv;
    this->service = (IUPnPService*)V_DISPATCH(&cv);
  }
  ~_MyUpnpService()
  {}
}MyUpnpService;

typedef struct _MyUpnpDevice
{
public:
  CComVariant cv;
  CComPtr<IUPnPDevice> device;
  std::vector<_MyUpnpDevice> subDevice;
  std::vector<MyUpnpService> service;
  _MyUpnpDevice(CComVariant &cv)
  {
    this->cv = cv;
    this->device = (IUPnPDevice*)V_DISPATCH(&cv);
  }
  ~_MyUpnpDevice()
  {
    service.clear();
    subDevice.clear();
  }
}MyUpnpDevice;
```

### 遍历跟设备

```C++
BOOL CMyUpnp::SearchRootDevices()
{
  IUPnPDeviceFinder* pUPnPDeviceFinder;
  HRESULT hr = CoCreateInstance(CLSID_UPnPDeviceFinder, NULL, CLSCTX_INPROC_SERVER,
    IID_IUPnPDeviceFinder, reinterpret_cast<void**>(&pUPnPDeviceFinder));
  if (SUCCEEDED(hr))
  {
    IUPnPDevices *devices = NULL;
    // TypeURI: 对应ST字段内容
    // 查询跟设备：upnp:rootdevice
    // 查询网关设备：urn:schemas-upnp-org:device:InternetGatewayDevice:1
    BSTR uri = SysAllocString(TEXT("urn:schemas-upnp-org:device:InternetGatewayDevice:1"));
    hr = pUPnPDeviceFinder->FindByType(uri, 0, &devices);
    SysFreeString(uri);
    if (SUCCEEDED(hr))
    {
      // 遍历根设备
      IEnumVARIANT *piEnum = NULL;
      hr = devices->get__NewEnum((IUnknown**)&piEnum);
      CComVariant var;
      ULONG nReturned = 0;
      while (piEnum->Next(1, &var, &nReturned) == S_OK)
      {
        m_rootDevices.push_back(var);
      }
      piEnum->Release();
    }
    pUPnPDeviceFinder->Release();
    return TRUE;
  }
  return FALSE;
}
```

### 遍历子设备

```C++
// device
void CMyUpnp::EnumSubDevices(MyUpnpDevice &device)
{
  device.subDevice.clear();
  EnumSubServices(device);
  IUPnPDevices *children;
  if (device.device->get_Children(&children) == S_OK)
  {
    IEnumVARIANT *piEnum = NULL;
    if (children->get__NewEnum((IUnknown**)&piEnum) == S_OK)
    {
      CComVariant var;
      ULONG nReturned = 0;
      while (piEnum->Next(1, &var, &nReturned) == S_OK)
      {
        device.subDevice.push_back(MyUpnpDevice(var));
        EnumSubDevices(device.subDevice.back());
      }
      piEnum->Release();
    }
    children->Release();
  }
}
```

### 遍历服务

```C++
void CMyUpnp::EnumSubServices(MyUpnpDevice &device)
{
  device.service.clear();
  // 遍历服务
  IUPnPServices* services = NULL;
  if (device.device->get_Services(&services) == S_OK)
  {
    IEnumVARIANT *piEnum = NULL;
    if (services->get__NewEnum((IUnknown**)&piEnum) == S_OK)
    {
      CComVariant var;
      ULONG nReturned = 0;
      while (piEnum->Next(1, &var, &nReturned) == S_OK)
      {
        device.service.push_back(var);
        IUPnPService *service = (IUPnPService*)V_DISPATCH(&var);
        BSTR tmp = NULL;
        if (service->get_ServiceTypeIdentifier(&tmp) == S_OK)
        {
          //cout << "get_ServiceTypeIdentifier\t\t" << CW2A(tmp) << endl;
          CString sn = tmp;
          if (sn == TEXT("urn:schemas-upnp-org:service:WANIPConnection:1") || sn == TEXT("urn:schemas-upnp-org:service:WANPPPConnection:1"))
          {
            // 这个就是端口映射服务
            m_connService = service;
          }
          SysFreeString(tmp);
        }
      }
      piEnum->Release();
    }
    services->Release();
  }
}
```

### 端口映射

```C++
// 服务接口：发送Action事件，反馈执行结果
BOOL CMyUpnp::InvokeAction(CString strAction, CComSafeArray<VARIANT> &arr, CComVariant &vaOutArgs, CComVariant &vaRetVal)
{
  if (!m_connService)
  {
    CheckSupportPortMapping();
    if (!m_connService)
      return FALSE;
  }
  CComVariant vaInActionArgs(*arr.GetSafeArrayPtr());
  BSTR act = strAction.AllocSysString();
  HRESULT re = m_connService->InvokeAction(act, vaInActionArgs, &vaOutArgs, &vaRetVal);
  if (re != S_OK)
  {
    if (re == DISP_E_TYPEMISMATCH)
      wcout << strAction.GetBuffer() << L" -> InvokeAction Error: 类型不匹配" << endl;
    else if(re == E_FAIL)
      wcout << strAction.GetBuffer() << L" -> InvokeAction Error: E_FAIL" << endl;
    else
    {
      wcout << strAction.GetBuffer() << L" -> InvokeAction Error: " << hex << re;
      if (vaRetVal.vt == VT_BSTR)
      {
        // 排除常规遍历提醒
        if (strAction != TEXT("GetGenericPortMappingEntry") || CString(V_BSTR(&vaRetVal)) != TEXT("SpecifiedArrayIndexInvalid"))
        {
          wcout << L" -> " << V_BSTR(&vaRetVal);
          m_lastError = V_BSTR(&vaRetVal);
        }
      }
      wcout << endl;
    }
  }
  SysFreeString(act);
  return re == S_OK;
}
```

```C++
EPortMapping CMyUpnp::AddPortMapping(CString localIP, DWORD localPort, DWORD remotePort, CString des, CString protocol, CString remoteHost)
{
  // 添加映射
  CString act = TEXT("AddPortMapping");
  CComSafeArray<VARIANT> saInArr;
  saInArr.Create();
  // 注意这里的参数顺序是固定的，一一对应到XML结构
  saInArr.Add(CComVariant(""));	// NewRemoteHost: 通常是空串
  saInArr.Add(CComVariant(remotePort));	// NewExternalPort
  saInArr.Add(CComVariant(protocol));		// NewProtocol: TCP|UDP
  saInArr.Add(CComVariant(localPort));	// NewInternalPort
  saInArr.Add(CComVariant(localIP));		// NewInternalClient
  saInArr.Add(CComVariant(VARIANT_TRUE));	// NewEnabled: 必须是 VARIANT_TRUE
  saInArr.Add(CComVariant(des.GetBuffer()));	// NewPortMappingDescription
  saInArr.Add(CComVariant("0"));			// NewLeaseDuration

  CComVariant vaOutArgs, vaRetVal;
  if (InvokeAction(act, saInArr, vaOutArgs, vaRetVal))
  {
    return PM_SUCCESS;
  }
  if (m_lastError == TEXT("ConflictInMappingEntry"))
    return PM_ERROR_PORT_CONFLICT;
  return PM_ERROR;
}
```

```C++

EPortMapping CMyUpnp::DeletePortMapping(DWORD remotePort, CString protocol, CString remoteHost)
{
  // 删除映射
  CString act = TEXT("DeletePortMapping");
  CComSafeArray<VARIANT> saInArr;
  saInArr.Create();
  // 注意这里的参数顺序是固定的，一一对应到XML结构
  saInArr.Add(CComVariant(remoteHost));	// NewRemoteHost: 通常是空串
  saInArr.Add(CComVariant(remotePort));	// NewExternalPort
  saInArr.Add(CComVariant(protocol));		// NewProtocol: TCP|UDP

  CComVariant vaOutArgs, vaRetVal;
  if (InvokeAction(act, saInArr, vaOutArgs, vaRetVal))
  {
    return PM_SUCCESS;
  }
  return PM_ERROR;
}
```

## 备注

+ 端口映射
  + **测试发现仅支持>=1024的端口，否则反馈端口冲突错误**
    + 端口映射服务也明确说明了这点，可以查UPNP官方文档，有XML和结构字段说明
  + **WinAPI所传参数和XML结构中的参数是一一对应的，并且顺序是固定的**
  + WinAPI封装了网络通讯，查找/遍历/添加映射/删除映射都是网络通讯，可以抓包分析明文XML加强理解
+ 测试映射
  + 通道打通后，内网端口开HTTP服务
  + 然后直接访问外网映射端口即可（外网映射端口只能外网访问）

## Demo

[UPNP](https://github.com/fxliu/VCDemo/tree/master/NET/Upnp)
