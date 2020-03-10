---
title: MySql
tags: 
    - MySql
categories: 
    - VC
description: MySql
date: 2020-03-03 10:27:37
updated: 2020-03-03 10:27:37
---

## 官网

+ [mysql环境](https://dev.mysql.com/downloads/installer/)
  + [指定版本](https://downloads.mysql.com/archives/community/)
  + C库下载5.x最新版即可，8只支持64位2019
  + zip包含的是低版本VS + /MDd参数编译结果lib和dll
  + 最好是自己下载源码编译
+ [官方文档](https://dev.mysql.com/doc/)

### 源码编译

+ [CMake](https://cmake.org/download/)
  + 下载windows版最新版即可，CMake只是生成VS编译环境，32/64位不影响结果
+ 解压后源码路径：`D:\mysql-5.7.28\mysql-5.7.28`
  + 创建目录：`D:\mysql-5.7.28\build`, `D:\mysql-5.7.28\install`
+ 运行cmake-gui
  + source: `D:\mysql-5.7.28\mysql-5.7.28`
  + build: `D:\mysql-5.7.28\build`
  + Configure编译
    + 错误处理：`You can download it with -DDOWNLOAD_BOOST=1 -DWITH_BOOST=<directory>`
      + 错误原因：需要下载boost，设置参数，自动下载即可
      + 选中`DOWNLOAD_BOOST`
      + 创建并设置`WITH_BOOST=D:\mysql-5.7.28\mysql-5.7.28\boost`
    + 参数调整 - 并创建对应目录
      + `CMAKE_INSTALL_PREFIX`:`D:/mysql-5.7.28/install`
      + `MYSQL_DATADIR`:`D:/mysql-5.7.28/install`
      + `MYSQL_KEYRINGDIR`:`D:/mysql-5.7.28/keyring`
    + SSL：根据体型路径下载安装
      + 自己编译OpenSSL
        + 目录结构：D:\openssl\include\openssl\*.h, D:\openssl\lib\*.lib
      + 指定SSL参数
        + `WITH_SSL`:`D:/openssl`
  + 重新编译Configure
    + 遇到错误自己看看错误描述和`cmake`文件夹下的编译脚本，比度娘靠谱

## 基础使用

```C++
// 只需要`libmysql.dll` `libmysql.lib` `mysqlclient.lib` 即可
#include "stdafx.h"
#include "MySqlClient.h"

CMySqlClient::CMySqlClient()
{
    m_sql = NULL;
}

CMySqlClient::~CMySqlClient()
{
}

bool CMySqlClient::Init()
{
    m_sql = mysql_init(NULL);
    if (!m_sql)
    {
        printf("mysql_init error.");
        return false;
    }
    // 设置编码
    // mysql_options(m_sql, MYSQL_SET_CHARSET_NAME, "gbk");
    return true;
}

void CMySqlClient::Release()
{
    if (!m_sql)
    {
        m_sql = NULL;
    }
}

bool CMySqlClient::Connect()
{
    if (!mysql_real_connect(m_sql, "127.0.0.1", "root", "12345678", NULL, 3306, NULL, NULL))
    {
        printf("mysql_real_connect error.");
        return false;
    }
    bool bQuery = true;
    if (mysql_query(m_sql, "SELECT * FROM testdb.test"))
    {
        bQuery = false;
        printf("mysql_query error: %s", mysql_error(m_sql));
    }
    MYSQL_RES *res = mysql_use_result(m_sql);
    if (res)
    {
        MYSQL_ROW row;
        while (row = mysql_fetch_row(res))
        {
            if (row == NULL)
                break;
            for (unsigned int c = 0; c < mysql_num_fields(res); c++)
            {
                printf("%s\t", row[c]);
            }
            printf("\n");
        }
        mysql_free_result(res);
    }
    mysql_close(m_sql);
    return bQuery;
}
```
