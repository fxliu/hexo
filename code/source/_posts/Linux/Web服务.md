---
title: Web服务
tags: 
  - Web服务
categories: 
  - linux
description: Web服务, apache, PHP, nginx
date: 2019-11-25 15:14:42
updated: 2019-11-25 15:14:42
---

## APACHE 部署

```sh
# yum封装
yumInstall(){
    install_name=$1
    local_fn=./install/$2
    if [ -f "$local_fn" ]
    then
        echo "yum localinstall $local_fn -y"
        yum localinstall $local_fn -y
    else
        echo "yum install $install_name -y"
        yum install $install_name -y
    fi
}
```

```sh
set -e
set -u
set -v
# 引入yum便捷安装脚本, 把已有rpm安装包复制到install子目录
../yum-install.sh

# wget升级
yum install openssl-devel -y
tar -zxvf wget-1.19.2.tar.gz
cd wget-1.19.2
./configure --prefix=/usr --sysconfdir=/etc --with-ssl=openssl
make
make install
cd ..

# apache
yumInstall httpd httpd-2.4.6-67.el7.centos.6.x86_64.rpm

# 安装 epel 安装源
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
# 安装 webtatic 安装源
wget https://mirror.webtatic.com/yum/el7/webtatic-release.rpm --no-check-certificate
rpm -Uvh webtatic-release.rpm
# 更新yum缓存
yum makecache fast

# 安装PHP7.2
yumInstall php72w mod_php72w-7.2.2-1.w7.x86_64.rpm
yumInstall php72w-cli php72w-cli-7.2.2-1.w7.x86_64.rpm
# 支持mysql
yumInstall php72w-mysql.x86_64 php72w-mysql-7.2.2-1.w7.x86_64.rpm

yum install php72w-gd
#=======================================================================================================
# apache配置: 关闭test页
echo "#" > /etc/httpd/conf.d/welcome.conf
sed -i 's/Options Indexes FollowSymLinks/Options FollowSymLinks/g' /etc/httpd/conf/httpd.conf
sed -i 's@ErrorLog "logs/error_log"@ErrorLog "|/usr/sbin/rotatelogs -l /var/log/httpd/error_log-%Y-%m-%d 86400"@g' /etc/httpd/conf/httpd.conf
sed -i '/CustomLog "logs\/access_log" combined/a\    CustomLog "|\/usr\/sbin\/rotatelogs -l \/var\/log\/httpd\/access_log-%Y-%m-%d 86400" combined env=!paichu' /etc/httpd/conf/httpd.conf
sed -i 's@CustomLog "logs/access_log" combined@SetEnvIf Request_URI "\.(html)$" paichu@g' /etc/httpd/conf/httpd.conf
sed -i 's@LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\"" combined@LogFormat "%{X-Forwarded-For}i %h %l %u %t \\"%m %U %q %H\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\"" combined@g' /etc/httpd/conf/httpd.conf
# PHP 时间策略调整
sed -i 's@;date.timezone.*@date.timezone=PRC@g' /etc/php.ini

# PHP 使用内存大小
sed -i 's@memory_limit.*@memory_limit = 512M@g' /etc/php.ini
# 执行优化
yumInstall php72w-opcache php72w-opcache-7.2.2-1.w7.x86_64.rpm
# 优化配置项: /etc/php.d/opcache.ini
sed -i 's/;\?opcache.memory_consumption=[0-9]*/opcache.memory_consumption=512/g' /etc/php.d/opcache.ini
sed -i 's/;\?opcache.validate_timestamps=[0-9]*/opcache.validate_timestamps=1/g' /etc/php.d/opcache.ini
sed -i 's/;\?opcache.revalidate_freq=[0-9]*/date.revalidate_freq=600/g' /etc/php.d/opcache.ini
sed -i 's/;\?opcache.save_comments=[0-9]*/date.save_comments=1/g' /etc/php.d/opcache.ini
sed -i 's/;\?opcache.load_comments=[0-9]*/date.load_comments=1/g' /etc/php.d/opcache.ini
# PHP优化
# 手动配置: sysctl vm.nr_hugepages=512
# sysctl vm.nr_hugepages: 查看配置值
# 查看分页情况: cat /proc/meminfo  | grep Huge
sed -i '/vm.nr_hugepages=.*/d' /etc/sysctl.conf
sed -i '$a\vm.nr_hugepages=512' /etc/sysctl.conf
sysctl -p
sed -i '/opcache.enable=1/a\opcache.huge_code_pages=1' /etc/php.d/opcache.ini
sed -i '/opcache.enable=1/a\opcache.file_cache=/tmp' /etc/php.d/opcache.ini
#=======================================================================================================
# SSL支持 - 走负载均衡
# yum install mod_ssl -y
# sed -i 's/#DocumentRoot/DocumentRoot/g' /etc/httpd/conf/httpd.conf
#=======================================================================================================
# 防火墙
systemctl start firewalld
systemctl enable firewalld.service
firewall-cmd --add-port=80/tcp --permanent
# 启用新配置
firewall-cmd --reload

# 启动httpd
systemctl start httpd
systemctl enable httpd.service

# 查看端口
# netstat -lntp
```

## NGINX 部署

+ 环境: Centos6.5
+ 软件: [nginx-1.6.0](http://nginx.org/en/download.html)
+ 位置: /usr/local/nginx
+ 方式: 源码编译安装

### 安装

```sh
# 编译环境
yum -y install gcc-c++
yum -y install zlib zlib-devel openssl openssl-devel pcre pcre-devel
# 卸载旧版本
cd /usr/local
find -name nginx
yum remove nginx
# 安装
tar -zxv -f nginx-1.6.0.tar.gz
cd nginx-1.6.0
./configure --prefix=/usr/local/nginx
make
make install
```

#### configure 参数

参数 | 说明
-------- | ---
--with-http_gzip_static_module | 启用HTTPGzip模块
--with-http_stub_status_module | 启用Nginxtatus功能，可以用来监控Nginx的当前状态
--with-http_realip_module | 获取真实IP
--with-http_addition_module | 向响应内容中追加内容
--with-http_sub_module | 替换相应内容（过滤器）
--with-http_dav_module | HTTP扩展动作支持（PUT, DELETE, MKCOL, COPY和MOVE）
--with-http_flv_module | FLV点播
--with-http_mp4_module | mp4点播
--with-http_gunzip_module --with-http_gzip_static_module | Gz压缩支持
--with-http_random_index_module | 随机首页配置
--with-http_secure_link_module | 安全连接检查
--with-mail --with-mail_ssl_module | 邮箱协议

#### 维护

```sh
#版本信息
/usr/local/nginx/sbin/nginx -V
#-t检查配置正确性
/usr/local/nginx/sbin/nginx -t
#-c指定配置文件位置
/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf
```

### 配置 nginx.conf

```sh
# Linux最大连接数调整
ulimit -n 65536
```

```conf
#运行用户，默认是nobody
user nobody nobody;
#指定Nginx要开启的进程数
#worker_processes auto;
worker_processes 4;
#日志。日志输出级别：debug、info、notice、warn、error、crit
#error_log logs/error.log notice;
#pid
#pid logs/nginx.pid
#更改worker进程的最大打开文件数限制。如果没设置的话，这个值为操作系统的限制。
#设置后你的操作系统和Nginx可以处理比“ulimit -a”更多的文件，
#所以把这个值设高，这样nginx就不会有“too many open files”问题了。
worker_rlimit_nofile 65535;


#events模块中包含nginx中所有处理连接的设置
events {
    #设置可由一个worker进程同时打开的最大连接数。默认1024
    #最大客户数也由系统的可用socket连接数限制（~ 64K），所以设置不切实际的高没什么好处。
    worker_connections 2048;
    #告诉nginx收到一个新连接通知后接受尽可能多的连接
    multi_accept on;
    #设置用于复用客户端线程的轮询方法：epoll、select、poll、kqueue、rtsig、/dev/poll
    use epoll;
}

http {
  #包含其他配置选项，一般要包含Nginx默认配置
  include       mime.types;
  #指定默认为二进制流
  default_type  application/octet-stream;
  #开启搞笑文件传输模式。将tcp_nopush和tcp_nodelay两个命令设置为“on”防止网络阻塞
  sendfile        on;
  tcp_nopush      on;
  tcp_nodelay     on;
  #客户端连接保持活动的超时时间
  keepalive_timeout     60;
  #客户端请求头读取超时时间
  client_header_timeout 10;
  #客户端请求主体读取超时时间
  client_body_timeout   10;
  #相应客户端的超时时间
  send_timeout          10;
  #是否启用gzip模块
  #gzip  on;

  #虚拟主机
  server {
      #端口
      listen       80;
      #IP或域名，多个域名之间用空格分开
      server_name  localhost;
      #设置网页的默认编码格式: gb2312
      #charset koi8-r;
      #访问日志存放路径
      #access_log  logs/host.access.log  main;

      #默认访问的首页地址
      index index.html index.htm index.jsp
      #网页根目录
      root /web/wwwroot/www.ixdba.net

      #地址匹配，支持正则
      location / {
          #对应网页根目录
          root   html;
          #默认首页
          index  index.html index.htm;
      }
  }
}

location /NginxStatus{
  #启用StubStatus的工作状态统计功能
  stub_status        on;
  #StubStatus日志
  access_log           logs/NginxStatus.log;
  #Nginx的一种认证机制（htpasswd命令）
  auth_basic           "NginxStatus"
  #用来制定认证的密码文件
  auth_basic_user_file ../htpasswd;
}

# 各种错误信息返回页面
error_page  404              /404.html;
error_page  500 502 503 504  /50x.html;
location = /50x.html {
  root   html;
}
```

#### 反向代理

```conf
http {
  server {
    location / {
      proxy_pass http://localhost:8000/;
    }
  }
}
```

#### 路径配置

```conf
# /i/logo.gif <==> /var/www/html/images/logo.gif
location /i {
  # 相对路径
  alias /var/www/html/images/;
}

# /download/ebook.tar.gz <==> /home/webdata/www/ebook.tar.gz
location ~ ^/download/(.*)$ {
  # 根路径
  root /home/webdata/www/$1
}

# 正则
#只匹配对/目录的额查询
location = / {...}
#匹配所有/开始的查询
location / {...}
#匹配已/images/开头的查询
location ^~ /images/ {...}
#匹配以gif、jpg、jpeg、swf结尾的文件
location ~* \.(gif|jpg|jpeg|swf)$ {...}

Location [=|~\~*|^~|@] /uri/{
  ..
}
# = ：完全匹配
# ~ ：字母大小写敏感
# ~*：忽略字母大小写
# ^~：只匹配前半部分
# @ ：内部重定向
```

#### 权限

```conf
location /images {
  root /var/....
  #允许目录遍历
  autoindex on；
  #显示文件字节数
  autoindex_exact_size off;
  #显示文件时间为服务器时间
  autoindex_localtime on;
}

# IP访问控制：依次匹配检查
location / {
  deny 192.168.66.80;
  allow 192.168.66.0/24;
  allow 192.16.88.0/16;
  deny all;
}

# 禁止访问某目录
location ~ ^/(WEB-INF)/ {
  deny all;
}

# 禁止访问某文件
location ~* \.(txt|doc)$ {
  root /data/www/wwwroot
  deny all
}

#限制GET请求：GET、POST、PUT、HEAD、OPTIONS...
limit_except GET{
  deny all;
}
```

#### SSL硬件加速

```sh
ssl_engine device;
#测试是否支持
openssl engine -t
```
