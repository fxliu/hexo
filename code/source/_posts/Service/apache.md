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
date: 2019-10-27 16:15:33
updated: 2019-10-27 16:15:33
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

## windows

```bat
:: 并发
:: 查看编译模块，mpm_*** 代表MPM模块
httpd -l

:: 配置 mpm_winnt
:: conf/httpd.conf 查找下属配置项，去掉该行前面的注释符号"#"
Include conf/extra/httpd-mpm.conf
:: conf/extra/httpd-mpm.conf
:: ThreadsPerChild: 每个子进程的最大并发线程数, 推荐设置：小型网站=1000 中型网站=1000~2000 大型网站=2000~3500
:: MaxRequestsPerChild: 每个子进程允许处理的请求总数, 该值设为0表示不限制请求总数(子进程永不结束)
<IfModule mpm_winnt_module>
ThreadsPerChild      2000
MaxRequestsPerChild    0 #推荐设置：小=10000 中或大=20000~100000
</IfModule>
```

```bat
:: 日志分割
:: 开启日志模块：conf/httpd.conf 查找下属配置项，去除前面的注释符号
LoadModule log_config_module modules/mod_log_config.so

:: 找到以下一行注释 #
CustomLog "logs/access.log" common
:: 按天分割日志改为
:: -l: 使用本地时间代替GMT时间作为时间基准
CustomLog "|bin/rotatelogs.exe -l logs/%Y_%m_%d.access.log 86400" common
:: 按天日志大小分割改为
CustomLog "|bin/rotatelogs.exe -l logs/%Y_%m_%d.access.log 2M" common
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

## ab

```sh
yum install apr-util
yum install yum-utils
yum install yum-utils.noarch
#解压提取ab程序
yumdownloader httpd-tools*
rpm2cpio httpd-*.rpm | cpio –idmv
#也可以直接安装httpd-tools
yum install httpd-tools
# ab 只支持http, abs支持https, 直接去官网下Windows版, bin文件夹内有
```

```sh
#-n 请求数
#-c 并发数
ab -n1000 -c100 http://www.baidu.com/

#请求数一定要大于并发数
#根据机器性能，通常并发数略小一些测试结果中秒级处理能力显的越高，请求数越多，秒级处理能力数字越准确

Document Length:      #请求文件长度
Concurrency Level:    #并发数量
Time taken for tests: #总时间
Complete requests:    #请求次数
Failed requests:      #失败请求
Total transferred:    #共传输字节
HTML transferred:     #实际传输字节
Requests per second:  #每秒请求数量-*-
Time per request:     #用户平均请求等待时间
Time per request:     #服务器平均处理时间
Transfer rate:        #每秒获取的数据长度
```

```sh
## Post 配置文件
ab -n1 -c1 -p ab_test_heart.txt -T application/x-www-form-urlencoded http://192.168.1.63/manager/api/sysinfo/

-T 指定数据格式
-p 指定数据文件

ab_test_heart.txt内容
info=***

不支持查询HTTP返回值, 使用抓包工具分析吧
```
