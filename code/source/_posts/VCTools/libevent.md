---
title: libevent
tags: 
    - libevent
categories: 
    - VC
description: libevent
date: 2022-05-06 01:39:56
updated: 2022-05-06 01:39:56
---

## 源码编译

```bat
:: 开始菜单 -> VS2015 开发人员命令提示
:: cd进入解压后的ibevent-2.1.11-stable目录下
nmake /f Makefile.nmake
:: 如果报错：f:\lib\libevent-2.1.11-stable\minheap-internal.h(73): error C2065: “UINT32_MAX”: 未声明的标识符
:: 在该文件(minheap-internal.h)中添加 #include “stdint.h”，再次编译

:: 复制生成的  libevent.lib libevent_core.lib libevent_extras.lib

:: 复制头文件, 到自己工程的 include 目录, 
:: libevent-2.1.11-stable\include
:: libevent-2.1.11-stable\WIN32-Code\nmake  // 会有重名文件, 直接覆盖即可
```

## Windows Demo

```C++
// 配置路径: ..\include\libevent
// stdafx.h
#define _WINSOCK_DEPRECATED_NO_WARNINGS 1   // 放在最上面

#include <iostream>
#include <string.h>
#include <WS2tcpip.h>
#include "libevent\event.h"
#include "libevent\event2\event.h"
#include "libevent\event2\bufferevent.h"
#include "libevent\event2\listener.h"
#include "libevent\event2\thread.h"
#include "libevent\event2\buffer.h"

// main.cpp
// ----------------------------------------------------------------------------
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "wsock32.lib")
#pragma comment(lib, "Iphlpapi.lib")
#pragma comment(lib, "libevent.lib")
#pragma comment(lib, "libevent_core.lib")
#pragma comment(lib, "libevent_extras.lib")

using namespace std;

/************************************
@ Brief:		读缓冲区回调
@ Author:		woniu201
@ Created:		2018/11/21
@ Return:
************************************/
void read_cb(struct bufferevent *bev, void *arg)
{
	char buf[1024] = { 0 };
	char* ip = (char*)arg;

	bufferevent_read(bev, buf, sizeof(buf));

	cout << "client " << ip << " say:" << buf << endl;

	//写数据给客户端
	const char *p = "i am server, i received your msg!";
	bufferevent_write(bev, p, strlen(p) + 1);

	// 处理完后退出
	event_base_loopexit(bufferevent_get_base(bev), NULL);
	// 立即退出
	// event_base_loopbreak(bufferevent_get_base(bev));
}

/************************************
@ Brief:		写缓冲区回调
@ Author:		woniu201
@ Created:		2018/11/21
@ Return:
************************************/
void write_cb(struct bufferevent *bev, void *arg)
{
	cout << "I'm 服务器，成功写数据给客户端，写缓冲回调函数被调用..." << endl;
}

/************************************
@ Brief:		事件回调
@ Author:		woniu201
@ Created:		2018/11/21
@ Return:
************************************/
void event_cb(struct bufferevent *bev, short events, void *arg)
{
	char* ip = (char*)arg;
	if (events & BEV_EVENT_EOF)
	{
		cout << "connection closed:" << ip << endl;
	}
	else if (events & BEV_EVENT_ERROR)
	{
		cout << "some other error !" << endl;
	}

	bufferevent_free(bev);
	cout << "bufferevent 资源已经被释放..." << endl;
}


/************************************
@ Brief:		监听回调
@ Author:		woniu201
@ Created:		2018/11/21
@ Return:
************************************/
void cb_listener(struct evconnlistener *listener, evutil_socket_t fd, struct sockaddr *addr, int len, void *ptr)
{
	struct sockaddr_in* client = (sockaddr_in*)addr;
	cout << "connect new client: " << inet_ntoa(client->sin_addr) << "::" << ntohs(client->sin_port) << endl;

	struct event_base *base = (struct event_base*)ptr;

	//添加新事件
	struct bufferevent *bev;
	bev = bufferevent_socket_new(base, fd, BEV_OPT_CLOSE_ON_FREE);

	//给bufferevent缓冲区设置回调
	bufferevent_setcb(bev, read_cb, write_cb, event_cb, inet_ntoa(client->sin_addr));

	//启动 bufferevent的 读缓冲区。默认是disable 的
	bufferevent_enable(bev, EV_READ | EV_PERSIST);
}

int test()
{
#ifdef WIN32
	WORD wVersionRequested;
	WSADATA wsaData;
	wVersionRequested = MAKEWORD(2, 2);
	(void)WSAStartup(wVersionRequested, &wsaData);
#endif
	//init server
	struct sockaddr_in serv;

	memset(&serv, 0, sizeof(serv));
	serv.sin_family = AF_INET;
	serv.sin_port = htons(8888);
	serv.sin_addr.s_addr = htonl(INADDR_ANY);

	// 启用Windows多线程
	evthread_use_windows_threads();
	// 配置IOCP
	struct event_config* cfg = event_config_new();
	event_config_set_flag(cfg, EVENT_BASE_FLAG_STARTUP_IOCP);
	event_config_set_num_cpus_hint(cfg, 10);	// 多线程个数

	//创建 event_base
	//struct event_base * base;
	//base = event_base_new();
	event_base *base;
	base = event_base_new_with_config(cfg);
	event_config_free(cfg);

	//创建套接字
	//绑定
	//接收连接请求
	struct evconnlistener* listener;
	listener = evconnlistener_new_bind(base, cb_listener, base, 
		LEV_OPT_CLOSE_ON_FREE | LEV_OPT_REUSEABLE, 
		36, (struct  sockaddr*)&serv, sizeof(serv));

	//启动循环监听
	event_base_dispatch(base);
	evconnlistener_free(listener);
	event_base_free(base);
	return 0;
}

```
