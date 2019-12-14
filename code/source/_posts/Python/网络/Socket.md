---
title: socket
tags: 
  - socket
categories: 
  - Python
description: socket
date: 2019-12-14 18:46:20
updated: 2019-12-14 18:46:20
---

## TCP

```py
# coding=gbk
import socket

def tcp_server_start():
    # socket.AF_INET (IPV4)
    # socket.SOCK_STREAM (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取本地主机名
    host = socket.gethostname()
    # 绑定端口 IP:port
    s.bind(('', 8080))

    # 最大允许连接数量
    s.listen(3)

    # 死循环，重复的处理着每个客户端的请求
    while True:
        # 阻塞 每当有客户端的请求过来开始执行
        # 连接处理 （已完成三次握手）并获取资源对象 | conn 请求对象 | addr 客户端地址 ip: port
        conn, addr = s.accept()

        # 请求处理 | 读取客户端发送过来的数据 | recv(1024) 指定每次读取 1024 字节，当数据较长时可以通过 while 循环读取
        data = conn.recv(1024)

        print data
        conn.send(data)
        conn.close()


def tcp_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8080))
    s.send("test")
    print s.recv(1024)
    s.close()

if __name__ == '__main__':
    tcp_server_start()
    # tcp_client()
```

## SocketServer

```py
# coding=gbk
import SocketServer

# 必须继承socketserver基类
class MyTcpHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print 'setup'

    # 重写基类里的handler()方法，在这个方法里处理接收、发送请求
    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                print("客户端退出！")
                break
            print(data)

            # 发送转换小写的数据给客户端，然后进入到下一个循环
            self.request.send(data)

    def finish(self):
        print 'finish'
1
if __name__ == '__main__':
    # 实例化socketserver，并传送服务器ip、port和子类
    # 单进程，单线程
    # my_server = SocketServer.TCPServer(('127.0.0.1', 8080), MyTcpHandler)
    # 单进程，多线程
    my_server = SocketServer.ThreadingTCPServer(('127.0.0.1', 8080), MyTcpHandler)
    # 多进程：linux
    # my_server = SocketServer.ForkingTCPServer(('127.0.0.1', 8080), MyTcpHandler)
    my_server.serve_forever()
```

## tornado TcpServer

[官网](https://www.tornadoweb.org/en/stable/)看Demo吧
tornado的多进程都是基于fork，仅支持Linux

[中文版](https://tornado-zh.readthedocs.io/zh/latest/index.html)

+ tornado.tcpserver
+ tornado.tcpclient
