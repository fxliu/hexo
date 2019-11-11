---
title: Django
tags: 
  - Django
categories: 
  - Python
description: Django
date: 2019-11-09 14:25:09
updated: 2019-11-09 14:25:09
---

## 安装

`pip install Django`

+ 命令行测试`python -m django --version`
+ Py脚本测试

```py
# py测试安装是否成功
import django
django.get_version()
```

## HelloWorld

+ 创建项目：`django-admin startproject mysite`
+ 启动项目：`python manage.py runserver`
  + 指定IP端口：`python manage.py runserver 127.0.0.1:8000`
+ 创建视图

```py
# hello.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world ! ")
```

+ 映射路径
  + 修改：urls.py

```py
# 导入 hello
from . import hello
# 映射路径
urlpatterns = [
    path('', hello.hello),
]
# 映射说明：正则写法
from django.urls import re_path
re_path('^hello.*$', view.hello)    # 所有hello开头的URI, 均映射到view.hello
```
