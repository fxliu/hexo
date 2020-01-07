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

## ORM - sqlalchemy

### sqlalchemy 安装

`pip3 install sqlalchemy`

### sqlalchemy 使用

```py
from sqlalchemy import create_engine
# 创建引擎: mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
egine=create_engine('mysql+pymysql://root@127.0.0.1/db1?charset=utf8')
# 执行SQL
egine.execute('create table if not EXISTS t1(id int PRIMARY KEY auto_increment,name char(32));')
cur=egine.execute('insert into t1 values(%s,%s);',[(1,"egon1"),(2,"egon2"),(3,"egon3")])
cur=egine.execute('insert into t1 values(%(id)s,%(name)s);',name='egon4',id=4)
# 新插入行的自增id
print(cur.lastrowid)

# 查询
cur=egine.execute('select * from t1')
cur.fetchone() #获取一行
cur.fetchmany(2) #获取多行
cur.fetchall() #获取所有行
```

```py
# 类 <==> 表
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,Enum,ForeignKey,UniqueConstraint,ForeignKeyConstraint,Index
from sqlalchemy.orm import sessionmaker

class Users(Base):
  # 表名
  __tablename__='users'
  # 字段：primary_key主键，autoincrement自增
  id=Column(Integer,primary_key=True,autoincrement=True)
  uname=Column(String(32),nullable=False,index=True)
  # nullable：字段是否可以为空，server_default：默认值，onupdate：行更新时值自动变化
  uptime = Column(TIMESTAMP(True), nullable=False, server_default=func.now(), onupdate=func.now())  

if __name__ == '__main__':
  egine=create_engine('mysql+pymysql://root@127.0.0.1:3306/db1?charset=utf8',max_overflow=5)
  # 创建所有表
  Base.metadata.create_all(egine)
  # 删除所有表
  Base.metadata.drop_all(egine)
  # 操作对象
  Session=sessionmaker(bind=egine)
  session=Session()
  # 新增
  session.add(Users(uname='张三'))
  session.add_all([Users(uname='张三'), Users(uname='李四')])
  session.commit()
  # 删
  session.query(Users).filter(Users.id > 3).delete()
  session.commit()
  # 改
  session.query(Users).filter(Users.id > 0).update({'uname':'哇哈哈'})
  session.commit()
  # 查
  res=session.query(Users).all()
  res=session.query(Users.uname).order_by(Users.id).all()
  res=session.query(Users.uname).first()
  res=session.query(Dep).filter(Users.id > 1,Users.id <1000)  # 默认为AND
  print([(row.id,row.dname) for row in res])
  # 过滤
  res=session.query(Emp).filter(~Emp.id.in_([1,3,99,101]),Emp.ename == '林海峰')  #~代表取反,转换成sql就是关键字not
  from sqlalchemy import and_,or_
  res=session.query(Emp).filter(and_(Emp.id > 0,Emp.ename=='林海峰')).all()
  res=session.query(Emp).filter(or_(Emp.id < 2,Emp.ename=='功夫熊猫')).all()
  # 通配符
  res=session.query(Emp).filter(Emp.ename.like('%海_%')).all()
  # limit
  res=session.query(Emp)[0:5:2]
  # 排序
  res=session.query(Emp).order_by(Emp.dep_id.desc(),Emp.id.asc()).all()
  # 分组
  from sqlalchemy.sql import func
  res=session.query(Emp.dep_id).group_by(Emp.dep_id).all()
  res=session.query(
      func.max(Emp.dep_id),
      func.min(Emp.dep_id),
      func.sum(Emp.dep_id),
      func.avg(Emp.dep_id),
      func.count(Emp.dep_id),
  ).group_by(Emp.dep_id).all()

  res=session.query(
      Emp.dep_id,
      func.count(1),
  ).group_by(Emp.dep_id).having(func.count(1) > 2).all()
  # 连表
  res=session.query(Emp,Dep).all()
  res=session.query(Emp,Dep).filter(Emp.dep_id==Dep.id).all()
  # 内连接
  res=session.query(Emp).join(Dep)
  # 左连接
  res=session.query(Emp.id,Emp.ename,Emp.dep_id,Dep.dname).join(Dep,isouter=True).all()
  # 组合
  q1=session.query(Emp.id,Emp.ename).filter(Emp.id > 0,Emp.id < 5)
  q2=session.query(Emp.id,Emp.ename).filter(
      or_(
          Emp.ename.like('%海%'),
          Emp.ename.like('%昊%'),
      )
  )
  res1=q1.union(q2) #组合+去重
  res2=q1.union_all(q2) #组合,不去重
  # 子查询
  res=session.query(
    session.query(Emp).filter(Emp.id > 8).subquery()
  ).all()
```
