---
title: 数据库
tags: 
  - pymysql
categories: 
  - Python
description: pymysql
date: 2019-11-11 14:27:12
updated: 2019-11-11 14:27:12
---

## 安装

`pip install pymysql`

## 常规使用

```py
import pymysql

# 连接
conn = pymysql.connect(
  host=db_info['ip'], user=db_info['user'], passwd=db_info['password'],
  port=port, db=db_info['dbname'], charset='utf8')
conn.autocommit(autocommit)   # 是否自动提交
cur = conn.cursor()

# 语句执行
cur.execute(sql)
# 事务提交
conn.commit()

# Select 结果
cur.fetchone()
cur.fetchmany(num)
cur.fetchall()

# insert / update / delete 影响个数
cur.rowcount
cur.rownumber
```

## Demo

[mysql](https://github.com/fxliu/Python/tree/master/%E6%95%B0%E6%8D%AE%E5%BA%93)
[sqlserver](https://github.com/fxliu/Python/tree/master/%E6%95%B0%E6%8D%AE%E5%BA%93)
