---
title: sqlite
tags: 
  - sqlite
categories: 
  - VC
description: sqlite
date: 2019-12-18 09:19:35
updated: 2019-12-18 09:19:35
---

## 部署

+ [官网下载](https://www.sqlite.org/download.html)
  + sqlite-snapshot-*.tar
  + sqlite-dll-win32-x86-*.zip
+ [DLL环境]
  + 解压`sqlite-dll-win32-x86-*.zip`得到`sqlite3.dll`+`sqlite3.def`
  + DLL同级目录执行如下指令得到lib：
    + `VS_PATH\bin\lib.exe /out:sqlite3.lib /MACHINE:IX86 /DEF:sqlite3.def`
  + 加压`sqlite-snapshot-*.tar`得到`sqlite3.h`
  + 复制`sqlite3.lib`+`sqlite3.h`到工程即可

## 简单案例

```C++
// 打开本地缓存库
CStringA strDB = CStringA(CW2A(GetRunPath()).m_psz) + "\\usbhid.db";
if (SQLITE_OK != sqlite3_open(strDB, &m_sql))
{
  LOG_HID_ERROR(TEXT("sqlite3打开失败，删除本地缓存，并重新创建"));
  DeleteFileA(strDB);
  if (SQLITE_OK != sqlite3_open(strDB, &m_sql))
  {
    LOG_HID_ERROR(TEXT("本地缓存库创建失败"));
    return FALSE;
  }
}
// 检查表，不存在则创建
char* errmsg = NULL;
if (sqlite3_exec(m_sql, R"(
  CREATE TABLE IF NOT EXISTS `idcard` (
    `uuid` varchar(16) NOT NULL,
    `info` varchar(320) NOT NULL,
    `uptm` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`uuid`)); )", NULL, NULL, &errmsg) != SQLITE_OK)
{
  LOG_HID_ERROR(TEXT("本地缓存表创建失败： %s"), CA2W(errmsg));
}
else
{
  // 清理1个月前缓存
  CString strTime = (CTime::GetCurrentTime() - CTimeSpan(365, 0, 0, 0)).Format(_T("%Y-%m-%d"));
  CString strSql;
  strSql.Format(TEXT("DELETE FROM idcard WHERE uptm<'%s'"), strTime);
  if (sqlite3_exec(m_sql, CW2A(strSql).m_psz, NULL, NULL, &errmsg) != SQLITE_OK)
  {
    LOG_HID_ERROR(TEXT("本地缓存表清理失败： %s"), CA2W(errmsg));
  }
}
// 回调
int ExecCallback(void* lpParam, int nCount, char** pValue, char** pName)
{
  CStringA &strResult = *(CStringA*)(lpParam);
  for (int index = 0; index < nCount; index++)
  {
    strResult += pValue[index];
    strResult += ",";
  }
  strResult += ";";
  return 0;
}
BOOL ******::Exec(CString strSql)
{
  char* errmsg = NULL;
  CStringA strResult;
  if (sqlite3_exec(m_sql, CW2A(strSql).m_psz, ExecCallback, &strResult, &errmsg) != SQLITE_OK)
  {
    LOG_HID_ERROR(TEXT("指令执行失败： %s"), errmsg);
    return FALSE;
  }
  LOG_HID_INFO(TEXT("指令执行成功： %s"), CA2W(strResult));
  return TRUE;
}
```
