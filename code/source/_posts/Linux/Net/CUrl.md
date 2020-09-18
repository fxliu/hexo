---
title: CURL
tags: 
  - CURL
categories: 
  - linux
description: CURL
date: 2020-07-16 19:14:10
updated: 2020-07-16 19:14:10
---

## 环境

```sh
# ubuntu
sudo apt-get install libcurl4-openssl-dev
sudo apt remove libcurl4-openssl-dev

# 头文件：/usr/include/curl
# 复制头文件 + libcurl.a 使用即可：包含SSL的全功能
```

```sh
# 官网下载源码包: 静态 + SSL，去掉FTP, TFTP, TELNET, SMTP, SMB, RTSP, POP3, IMAP, GOPHER, DICT等模块
./configure --enable-shared=no --enable-static --with-ssl --disable-debug --disable-ftp --disable-tftp --disable-telnet --disable-smtp --disable-smb --disable-rtsp --disable-pop3 --disable-imap --disable-gopher --disable-dict

make
make install

# ubuntu /usr/local/lib/pkgconfig/libcurl.pc
-lcurl -lssl -lcrypto -lz -lpthread
-static
```

## Demo

`es:svn\bar_machine\trunk\C++\EIDSDK\linux`
`git:GitHub\VCDemo\Linux\Net`
