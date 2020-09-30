---
title: miracl
tags: 
  - miracl
categories: 
  - VC
description: miracl
date: 2020-09-30 09:28:48
updated: 2020-09-30 09:28:48
---

### 工具

[MIRACL](https://github.com/miracl/MIRACL)
[Visual Studio下编译和使用Miracl](https://www.jianshu.com/p/1aed3590b65b)
[SM2](https://github.com/khaosi/sm234)

### 编译

```md
新建项目`miracl`，选择“静态库”，不使用预编译头
点击“头文件”选项夹，除了选择`miracl.h`和`mirdef.h`外，还要加上`big.h`, `ec2.h`, `ecn.h`, `flash.h`, `zzn.h`。
    注意观察：`ms32doit.bat`：`copy mirdef.h32 mirdef.h`
点击“源文件”选项夹，添加现有项
    此处需要注意，在添加`source file`的时候请参照`ms32doit.bat`里面的C 文件列表
    注意观察：`ms32doit.bat`：`copy mrmuldv.c32 mrmuldv.c`
    点击“生成”，编译生成了`miracl.lib`
```
