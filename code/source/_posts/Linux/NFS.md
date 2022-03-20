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

## linux 部署

```sh
# 1号机安装NFS服务, 并设置为自启动
yum install nfs-utils rpcbind
vi /etc/exports
/home/work 10.255.48.33(rw)
systemctl enable nfs
systemctl start nfs

# 注意修改目录权限
chown nfsnobody.nfsnobody -R /data/imgdb/
chmod 777 -R /data/imgdb/

# 2号机自动挂载
yum -y install nfs-utils
showmount -e 172.19.189.192  // 查看共享
mount -t nfs 172.19.189.192:/data/imgdb /data/imgdb   // 手动挂载
mount -t nfs 192.168.0.201:/home/sun/nfs /es/nfs -o nolock
echo "172.19.189.192:/data/imgdb /data/imgdb nfs defaults 0 0" >> /etc/fstab   // 开机自动挂载
```
