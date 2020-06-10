---
title: RabbitMQ
tags: 
  - RabbitMQ
categories: 
  - RabbitMQ
description: RabbitMQ, httpapi
date: 2019-11-25 14:32:34
updated: 2020-01-13 15:09:10
---

## 常用

```sh
# 队列数据量
rabbitmqctl list_queues
rabbitmqctl list_queues | awk '{if($2!=0) {print $0}}'
rabbitmqctl list_queues | awk '{if($2>10) {print $0}}'
rabbitmqctl list_queues | grep 3701028953
rabbitmqctl list_connections | awk '{if($1=="weixin_new") {print $0}}'

ps -aux | grep 'netbar_report' | awk '{print $2}' | xargs kill

```

## 安装

`pip install pika`

+ Broker：简单来说就是消息队列服务器实体。
+ Exchange：消息交换机，它指定消息按什么规则，路由到哪个队列。
+ Queue：消息队列载体，每个消息都会被投入到一个或多个队列。
+ Binding：绑定，它的作用就是把exchange和queue按照路由规则绑定起来。
+ Routing Key：路由关键字，exchange根据这个关键字进行消息投递。
+ vhost：虚拟主机，一个broker里可以开设多个vhost，用作不同用户的权限分离。
+ producer：消息生产者，就是投递消息的程序。
+ consumer：消息消费者，就是接受消息的程序。
+ channel：消息通道，在客户端的每个连接里，可建立多个channel，每个channel代表一个会话任务

### Windows配置

rabbitmq自带管理后台，安装后需要配置开启

+ 进入rabbitmq安装目录中的sbin目录执行`rabbitmq-plugins enable rabbitmq_management`
  + 重启 `systemctl restart rabbitmq-server.service`
  + 配置远程rabbit访问：修改 `ebin/rabbit.app`
  + 找到loopback_users里的<<"guest">>并删除。
  + 重启 `systemctl restart rabbitmq-server.service`
+ 常用指令
  + 停止 `net stop RabbitMQ`
  + 启动 `net start RabbitMQ`
  + 如果上面的重启命令不起作用，使用 net stop RabbitMQ && net start RabbitMQ
+ 设置远程访问
  + 配置之前需要先添加用户，用于外网的访问
  + 通过web管理页面来添加用户和密码，使用`guest`登录web管理页面
    + `http://localhost:15672`
    + 进入`admin`标签页，然后点击`Add a user`
    + 输入新建的帐号密码，然后选择用户角色tags（选admin）;
  + 授权
    + 在Admin标签页下点击新增的用户 "用户名"，进入授权页面(默认直接点击"set permission"即可)
  + 用户以及授权添加完成之后，在etc/rabbitmq.config.example文件中，添加以下内容
    + {tcp_listeners, [5672]},
    + {loopback_users, ["admin"]},
      + `admin`为用户名
    + 保存后重启RabbitMQ服务
      + 如果不能保存，请先停止rabbitmq服务
  + 在浏览器中输入`http://127.0.0.1:15672`实现通过IP地址访问，成功登录
    + 如不能访问 请检查防火墙

### Centos7安装

```sh
# 本地文件存在则使用安装包，否则下载安装
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
. ./yum-install.sh
#==============================================
# rabbitmq服务
yumInstall erlang erlang-R16B-03.18.el7.x86_64.rpm
yumInstall rabbitmq-server.noarch rabbitmq-server-3.3.5-34.el7.noarch.rpm
#==============================================
# amqp支持
yumInstall php72w-devel.x86_64 php72w-devel-7.2.2-1.w7.x86_64.rpm     #目的是准备phpize命令

# wget -c https://github.com/alanxz/rabbitmq-c/releases/download/v0.8.0/rabbitmq-c-0.8.0.tar.gz
tar zxvf rabbitmq-c-0.8.0.tar.gz
cd rabbitmq-c-0.8.0
./configure --prefix=/usr/local/rabbitmq-c-0.8.0    # 指定安装目录
make && make install

# wget -c http://pecl.php.net/get/amqp-1.7.0.tgz     # pecl install amqp-1.7.0.tgz
tar zxf amqp-1.7.0.tgz
cd amqp-1.7.0
phpize
./configure --with-php-config=/usr/bin/php-config --with-amqp --with-librabbitmq-dir=/usr/local/rabbitmq-c-0.8.0/
make && make install

# 修改php.ini 加入：extension=amqp.so
echo extension=amqp.so > /etc/php.d/amqp.ini
#==============================================
systemctl start rabbitmq-server.service
systemctl enable rabbitmq-server.service

rabbitmq-plugins enable rabbitmq_management # 启用Web控制台
systemctl restart rabbitmq-server.service

rabbitmqctl delete_user guest

systemctl restart rabbitmq-server.service
rabbitmqctl set_policy policy "^" '{"ha-mode":"all"}'
#==============================================
# 调整防火墙
# rabbitmq - Web
# firewall-cmd --permanent --add-rich-rule 'rule family=ipv4 source address=172.19.0.0/16 port port=15672 protocol=tcp accept'
firewall-cmd --add-port=15672/tcp --permanent
# rabbitmq
firewall-cmd --add-port=5672/tcp --permanent
# rabbitmq 集群
firewall-cmd --permanent --add-rich-rule 'rule family=ipv4 source address=172.19.0.0/16 port port=4369 protocol=tcp accept'
firewall-cmd --permanent --add-rich-rule 'rule family=ipv4 source address=172.19.0.0/16 port port=25672 protocol=tcp accept'
firewall-cmd --reload
```

### Centos7集群

+ 集群 => join_cluster 需要根据域名配置
+ 修改hostname, N调整为对应数字
  + `hostnamectl set-hostname dianduweixin-ecsN`
+ 集群所有机器配置调整: 内网IP 与 hostname对应
  + `vi /etc/hosts`
+ 复制主节点cookie到所有子节点, 并重启服务
  + `scp /var/lib/rabbitmq/.erlang.cookie root@ip:/var/lib/rabbitmq/.erlang.cookie.1`
  + `systemctl restart rabbitmq-server.service`
+ 登录子节点, cookies改名, 并调整权限
  + `mv /var/lib/rabbitmq/.erlang.cookie /var/lib/rabbitmq/.erlang.cookie.bak`
  + `mv /var/lib/rabbitmq/.erlang.cookie.1 /var/lib/rabbitmq/.erlang.cookie`
  + `chown rabbitmq /var/lib/rabbitmq/.erlang.cookie`
  + `chgrp rabbitmq /var/lib/rabbitmq/.erlang.cookie`
  + `chmod 400 /var/lib/rabbitmq/.erlang.cookie`
  + `systemctl restart rabbitmq-server.service`
  + 备注：一定要调整为指定权限，否则cookie文件不生效
+ 子节点 添加到集群
  + `rabbitmqctl stop_app`
  + `rabbitmqctl reset`
  + `rabbitmqctl join_cluster rabbit@dianduweixin-ecs1`
  + `rabbitmqctl start_app`
+ 确认节点添加成功
  + `rabbitmqctl cluster_status`
+ 确认用户名
  + `rabbitmqctl list_users`
+ 确认镜像策略(WEB)
  + 删除guest `rabbitmqctl delete_user guest`
  + 追加用户 `rabbitmqctl add_user (用户名) (密码)`
  + 调整权限
    + `rabbitmqctl set_user_tags (用户名) administrator`
    + `rabbitmqctl set_permissions -p / (用户名) ".*" ".*" ".*"`
+ 文件连接数
  + 查看: `rabbitmqctl status`
    + {total_limit,19900},
    + {total_used,394},
    + {sockets_limit,17908},
    + {sockets_used,392},
+ 最大内存占用 `/etc/rabbitmq/rabbitmq.config`
  + `vm_memory_high_watermark` 改为 `0.8`
  + `heartbeat` 改为 `600`
  + `rabbitmqctl set_vm_memory_high_watermark 0.8`: 命令行即时生效, 不写入配置文件，重启就无效了
+ 通过修改sysctl配置，提高系统的打开文件数量
  + `vi /etc/sysctl.conf` 添加 `fs.file-max = 65535`
  + 系统配置重载 `sysctl -p`
+ 修改rabbitmq配置
  + `vi /etc/systemd/system/multi-user.target.wants/rabbitmq-server.service`
  + 在[Service]中，增加 `LimitNOFILE=20000`
+ 重启rabbitmq
  + `systemctl daemon-reload`
  + `systemctl restart rabbitmq-server`

### 集群重启

```sh
# 集群重启时，最后一个挂掉的节点应该第一个重启
# 如果因特殊原因（比如同时断电），而不知道哪个节点最后一个挂掉。可用以下方法重启：
# 先在一个节点上执行
rabbitmqctl force_boot
service rabbitmq-server start
#在其他节点上执行
service rabbitmq-server start
#查看cluster状态是否正常（要在所有节点上查询）。
rabbitmqctl cluster_status
#如果有节点没加入集群，可以先退出集群，然后再重新加入集群。

#上述方法不适合内存节点重启，内存节点重启的时候是会去磁盘节点同步数据，如果磁盘节点没起来，内存节点一直失败。
```

### 退出集群

```sh
#假设要把rabbitmq2退出集群, 在rabbitmq2上执行
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app

#在集群主节点上执行
rabbitmqctl forget_cluster_node rabbit@rabbitmq2
```

### 重装

```sh
# erlang
yum remove erlang
yum install erlang-R16B-03.18.el7.x86_64.rpm
# RabbitMQ
yum remove rabbitmq-server
yum install rabbitmq-server-3.3.5-34.el7.noarch.rpm
# rabbitmqctl status

# 指定nodename: 创建 /etc/rabbitmq/rabbitmq-env.conf, 并添加如下字符串
NODENAME=rabbitmq@dianduweixin-ecs1

# 测试启动
rabbitmq-server start
# 如果提示权限不够: chmod -R 777 /var/lib/rabbitmq/mnesia/
# 启动成功的话, Ctrl+C关闭, systemctrl启动即可
```

## Windows

```sh
# 官网下载并安装Erlang Windows环境 - 路径中不能包含空格
# 官网下载并安装rabbitmq-server Windows环境 - 路径中不能包含空格

# 服务停止|开启
rabbitmq-service.bat stop|start

# 配置文件路径: C:\Users\%USERNAME%\AppData\Roaming

# 命令行: http://www.rabbitmq.com/manpages.html
# 启用Web插件 - 需要重启服务: http://localhost:15672/
rabbitmq-plugins enable rabbitmq_management

# 安装服务 - Windows版安装后, 默认安装服务并启动
rabbitmq-service.bat install
# 删除服务
rabbitmq-service.bat remove
# 其他参数
help/start/strop/disable/enable

# rabbitmqctl:
# 将 %HOMEDRIVE%%HOMEPATH%\.erlang.cookie 或者 %USERPROFILE%\.erlang.cookie
# 拷贝到 C:\Windows\System32\config\systemprofile\.erlang.cookie ，然后重新启动

# 否则rabbitmqctl不可用: TCP connection succeeded but Erlang distribution failed
# 增加用户
rabbitmqctl.bat add_user user password
rabbitmqctl set_user_tags user administrator
rabbitmqctl set_permissions -p / user ".*" ".*" ".*"
# 删除用户
rabbitmqctl.bat delete_user user
# 其他命令
```

## 配置文件

```sh
# rabbitmq.config默认是没有生成的，只有一个rabbitmq.config.example，需要自己建一个，其实就是把.example拿掉就是了
# rabbitmq.config目录并非安装目录下面的etc, 默认是在 C:\Users\%USERNAME%\AppData\Roaming\RabbitMQ 下
# 调整心跳: 去掉{heartbeat, 86400} 前面的%%. 注意 如果当前大节点下面就这一个节点，后面逗号是必须拿掉的。
# 修改了配置文件后，停止服务 -> 重装服务 -> 启动服务, 才能生效
```

## rabbitmqadmin.py

```sh
# http://server-name:15672/cli 页面下载 rabbitmqadmin
# 拷贝到 /usr/local/bin 路径，并增加可执行权限，chmod 777 rabbitmqadmin
rabbitmqadmin --help
# 显示rabbitmqadmin的各种命令
rabbitmqadmin help subcommands

# 清空队列
rabbitmqadmin.py --host=127.0.0.1 --port=15672 --username=lfx --password=liufuxiang purge queue name=olcustomer_history
rabbitmqadmin.py --host=wx.dnndo.com --ssl --port=15443 --username=sys --password=c2s0iltx6DHZLrdW5V3SBFmb purge queue name=test
# 删除队列
rabbitmqadmin.py --host=wx.dnndo.com --ssl --port=15443 --username=sys --password=c2s0iltx6DHZLrdW5V3SBFmb delete queue name=test
```
