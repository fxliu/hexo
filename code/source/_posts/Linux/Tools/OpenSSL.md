---
title: OpenSSL
tags: 
  - OpenSSL
  - SM2
categories: 
  - linux
description: OpenSSL, SM2
date: 2020-09-15 16:29:49
updated: 2020-09-15 16:29:49
---

## 工具

+ [openssl](https://github.com/openssl/openssl)
  + Demo Tags：openssl-3.0.0-alpha6

## linux 环境

```sh
# 见INSTALL.md
./Configure
make
make install # as root, or using sudo

# 清理
make clean
make uninstall
```

## SM2

`基于OpenSSL1.1: https://github.com/greendow/SM2-encrypt-and-decrypt`
`es:svn\bar_machine\trunk\C++\EIDSDK\linux\ESEID`

`大牛封装sm2(基于OpenSSL),3,4: https://github.com/NEWPLAN/SMx`

`安装后说明文档：/usr/local/share/doc/openssl/html/man7/sm2.html`

```sh
./config no-deprecated --release no-afalgeng no-autoalginit no-autoerrinit no-autoload-config no-capieng no-cms no-comp no-ct no-dgram no-dso no-devcryptoeng no-engine no-err no-filenames no-gost no-hw-padlock no-makedepend no-multiblock no-nextprotoneg no-ocsp no-pic no-posix-io no-psk no-rdrand no-rfc3779 no-shared no-sock no-srp no-srtp no-sse2 no-static-engine no-tests no-threads no-ts no-ui-console no-ssl no-tls no-dtls no-aria no-bf no-blake2 no-camellia no-cast no-chacha no-cmac no-des no-dh no-dsa no-ecdh no-ecdsa no-idea no-md4 no-mdc2 no-ocb no-poly1305 no-rc2 no-rc4 no-rmd160 no-scrypt no-seed no-siphash no-whirlpool
```

```sh
# 交叉编译
./configure --host=arm-linux-gnueabihf --prefix=/home/lfx/eudev-master/build CC=arm-linux-gnueabihf-gcc AR=arm-linux-gnueabihf-ar
```
