---
title: Web服务
tags: 
  - Web服务
categories: 
  - linux
description: Web服务, apache, PHP
date: 2019-11-25 15:14:42
updated: 2019-11-25 15:14:42
---

## 部署

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
