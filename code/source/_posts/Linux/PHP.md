---
title: NFS
tags: 
  - NFS
categories: 
  - linux
description: NFS
date: 2020-07-16 19:14:10
updated: 2020-07-16 19:14:10
---

## 默认配置文件

```sh
# /etc/php.ini

# PHP 时间策略调整
sed -i 's@;date.timezone.*@date.timezone=PRC@g' /etc/php.ini
# PHP 使用内存大小
sed -i 's@memory_limit.*@memory_limit = 512M@g' /etc/php.ini

# session目录
session.save_path = "/tmp"
# apache可以修改：/etc/httpd/conf.d/php.conf
php_value session.save_path    "/var/lib/php/session"
```
