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
