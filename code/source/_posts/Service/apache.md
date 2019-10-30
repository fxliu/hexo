---
title: apache
tags: 
  - apache
  - goaccess
  - 日志
categories: 
  - service
  - linux
description: apache,goaccess,日志分析
date: 2019-10-27 ‏‎16:15:33
updated: 2019-10-27 ‏‎16:15:33
---

## apache

```sh
# -- Centos7 --
# 默认配置文件
/etc/httpd/conf/httpd.conf

# 默认日志位置
/var/log/httpd/
/etc/httpd/logs/ -> /var/log/httpd/

```

## goaccess

```sh
yum install goaccess -y
# 配置文件
/etc/goaccess.conf

# 分析
goaccess --config-file=/etc/goaccess.conf --output /var/www/html/goaccess.html /var/log/httpd/access_log-2018-11-28
# 多文件：尾部指定多个文件名
goaccess --config-file=/etc/goaccess.conf --output /var/www/html/goaccess/2018-04-14.html access_log-2018-11-28 access_log-2018-11-29
# 多文件：cat合并
cat access_log-* | goaccess --config-file=/etc/goaccess.conf --output /var/www/html/all.html
```

```conf
# 时间格式: 根据apache当前日志格式对应调整, [26/Oct/2019:23:59:59 +0800]
time-format %H:%M:%S
date-format %d/%b/%Y

# 日志格式 - 从http.conf中提取
# %{X-Forwarded-For}i %h %l %u %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"
# "%{X-Forwarded-For}i %h %l %u %t \"%m %U %q %H\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
# 222.171.180.161 100.116.227.226 - - [03/Apr/2018:14:29:33 +0800] "POST /wechat/2dBarCode.php HTTP/1.1" 200 262 "-" "-"
log-format %h %^ %l %u %^[%d:%t %^] "%r" %s %b "%R" "%^"

# 是否需要实时刷新
real-time-html true
```
