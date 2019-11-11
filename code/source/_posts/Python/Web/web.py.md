---
title: web.py
tags: 
  - web.py
categories: 
  - Python
description: web.py
date: 2019-11-11 13:51:44
updated: 2019-11-11 13:51:44
---

## 安装

`pip install web.py`

## hello world

+ 端口: 默认`8080`, 可以通过命令行修改 `python test.py 8081`
+ 发现HTTP请求时，创建新进程，所以**脚本更新，即时生效**

```py
# Hello world
import web

urls = ("/.*", "hello")   # 与类名相对应，大小写敏感
app = web.application(urls, globals())

class hello:
    def GET(self):
        return 'Hello, world!'

if __name__ == "__main__":
    app.run()
```

## 常规用法

```py
class hello:
  def GET(self):
    data = web.input()  # URL上报所有参数，包含post，get，表单
    return 'Hello, world!'
```

## 数据库

```py
db = web.database(
    dbn='mysql', host='localhost', port=3306,
    db='test_db', user='test', passwd='123456')

data = db.select("test_table")
for d in data:
    print(d['name'])
```
