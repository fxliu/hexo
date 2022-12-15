---
title: tools
tags: 
  - tools
categories: 
  - PHP
description: tools
date: 2022-12-14 13:05:01
updated: 2022-12-14 13:05:01
---

## 日志

```php
function eslog($msg, $fn="./log.log") {
	$now= date("Y-m-d H:i:s");
	error_log("[{$now}] ".$msg."\n\r",3,$fn);
}
```

## 随即字符串

```php
/**
 * 生成随机字符串
 */
function getrandstr($length){
	$str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890';
	//打乱字符串
	$randStr = str_shuffle($str);
	//substr(string,start,length);返回字符串的一部分
	$rands= substr($randStr,0,$length);
	return $rands;
}
```