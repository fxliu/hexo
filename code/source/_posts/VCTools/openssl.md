---
title: openssl
tags: 
  - openssl
categories: 
  - VC
description: VC, openssl
date: 2019-09-07 16:51:20
updated: 2020-01-04 18:01:30
---

## 编译

+ [官网](http://www.openssl.org/)
+ 编译工具
  + [ActivePerl](http://www.perl.org)
+ 环境
  + ActivePerl-5.16.2.1602-MSWin32-x86-296513.msi
  + openssl-1.0.1e

### 编译过程

```bat
:: 启动VS"开发人员命令提示"工具：nmake等指令环境
:: 文件位置：C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Visual Studio 2015\Visual Studio Tools\VS2015 开发人员命令提示.lnk
:: 快捷方式指向位置：%comspec% /k ""E:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\Tools\VsDevCmd.bat""

:: perl编译根目录必须是openssl的根目录
cd c:\openssl-1.0.1e
:: 运行configure，--prefix 指定编译目录(保存编译结果), no-asm表示不用汇编
:: VC-WIN32 代表release版，debug-VC-WIN32 代表Debug版
perl Configure VC-WIN32 --prefix=.\build_release
:: 创建MakeFile, perl中如果使用no-asm，这里替换为 ms\do_nasm.bat
ms\do_ms.bat

:: 64位
:; Configure参数调整：VC-WIN64A、debug-VC-WIN64A
:: ms\do_win64a.bat


:: 编译动态库- 默认/MD
nmake -f ms\ntdll.mak
:: 编译静态库 - 默认/MT
nmake -f ms\nt.mak
:: 测试动态库
nmake -f ms\ntdll.mak test
:: 测试静态库
nmake -f ms\nt.mak test

:: 安装动态库
nmake -f ms\ntdll.mak install
:: 安装静态库
nmake -f ms\nt.mak install

:: 清除上次动态库的编译，以便重新编译, 清理动态库
nmake -f ms\ntdll.mak clean
:: 清除上次静态库的编译，以便重新编译：清理静态库
nmake -f ms\nt.mak clean
```

### 编译配置

```bat
:: 编辑文件 ms\nt.mak，将该文件第19行与工程编译：C/C++ -> 代码生成 -> 运行库 相匹配
:: 搜索替换即可：CFLAG= /MD .....
:: 编辑选项=/MD->/MT

C Runtime Library：
/MD       MSVCRT.LIB      多线程DLL的Release版本
/MDd      MSVCRTD.LIB     多线程DLL的Debug版本
/MT       LIBCMT.LIB      多线程静态链接的Release版本
/MTd      LIBCMTD.LIB     多线程静态链接的Debug版本
/clr      MSVCMRT.LIB     托管代码和非托管代码混合
/clr:pure MSVCURT.LIB     纯托管代码

C++ Standard Library：
/MD       MSVCPRT.LIB     多线程DLL的Release版本
/MDd      MSVCPRTD.LIB    多线程DLL的Debug版本
/MT       LIBCPMT.LIB     多线程静态链接的Release版本
/MTd      LIBCPMTD.LIB    多线程静态链接的Debug版本
```

## VS应用

```C++
#include "openssl/aes.h"

// SSL依赖库
#pragma comment(lib, "IPHLPAPI.lib")
#pragma comment(lib, "Snmpapi.lib")
#pragma comment(lib, "netapi32.lib")

#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "wldap32.lib")
#pragma comment(lib, "Crypt32.lib")
// SSL库
#pragma comment(lib, "libeay32.lib")
#pragma comment(lib, "ssleay32.lib")
```

### CFB 128 NoPadding

```C++
#define CFB_KEY "0123456789012345"
#define CFB_VI "0123456789012345"

BOOL my_cfb128_encrypt(CStringA strIn, CStringA &strOut, unsigned char *ckey, unsigned char *ivec)
{
  AES_KEY keyEn;
  AES_set_encrypt_key(ckey, 128, &keyEn);
  unsigned char *szData = new unsigned char[strIn.GetLength()];
  memset(szData, 0, strIn.GetLength());
  memcpy(szData, strIn.GetBuffer(), strIn.GetLength());
  int num = 0;
  AES_cfb128_encrypt(szData, szData, strIn.GetLength(), &keyEn, ivec, &num, AES_ENCRYPT);
  std::string strBase64;
  nbase::Base64Encode((const char*)szData, strIn.GetLength(), &strBase64);
  delete szData;
  strOut = strBase64.c_str();
  return !strOut.IsEmpty();
}
BOOL my_cfb128_decrypt(CStringA strIn, CStringA &strOut, unsigned char *ckey, unsigned char *ivec)
{
  std::string strSrc;
  if (!nbase::Base64Decode(strIn.GetBuffer(), &strSrc))
    return FALSE;

  AES_KEY keyEn;
  AES_set_encrypt_key(ckey, 128, &keyEn);
  unsigned char *szData = new unsigned char[strSrc.size() + 1];
  memset(szData, 0, strSrc.size() + 1);
  memcpy(szData, strSrc.c_str(), strSrc.size());
  int num = 0;
  AES_cfb128_encrypt(szData, szData, strSrc.size(), &keyEn, ivec, &num, AES_DECRYPT);
  strOut.SetString((char*)szData, strSrc.size()); // 支持解密后二进制数据保存到CStringA
  delete szData;
  return !strOut.IsEmpty();
}
```
