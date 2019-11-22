---
title: MySQL
tags: 
  - SQL
categories: 
  - MySQL
description: SQL
date: 2019-10-27 13:53:32
updated: 2019-10-27 13:53:32
---

## 安装

```sh
# 服务指令
service mysqld start|stop|status
#---- 默认配置 ----
#程序位置
/usr/bin
#数据位置（配置+数据库）
/var/lib/mysql
#运行日志（查看错误）
/var/log/mysqld.log
#配置文件：一般不动
/etc/my.cnf
```

### Centos7

```sh
wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
yum install mysql57-community-release-el7-11.noarch.rpm
yum repolist enabled
yum install mysql-community-server

# 默认密码:
grep 'temporary password' /var/log/mysqld.log

# 关闭密码策略:
vi /etc/my.conf
# 追加:
validate_password=off

# 超管密码
mysql -uroot -p
# 修改密码:
set password for 'root'@'localhost'=password('easysoft');
```

### 配置/状态

```sql
-- 状态
SHOW STATUS;
SHOW STATUS LIKE "threads%";
-- 参数
show variables;
show variables like "%heap%";
show variables like "tmp_table_size";
-- 设置参数
SET max_heap_table_size = 1024*1024;
-- 参数
default_storage_engine    -- 默认引擎

-- 所有引擎
SHOW ENGINES;
```

## 常规Demo

+ 表复制: `INSERT INTO t1 SELECT * FROM t2`

## 字符串

```SQL
-- REPLACE
SELECT REPLACE('aaa.mysql.com','a','w');
```

```sql
LEFT() RIGHT() --左边或者右边的字符
LOWER() UPPER() --转换为小写或者大写
LTRIM() RTIM() --去除左边或者右边的空格
LENGTH() --长度

-- 字符串 组合
CONCAT('bar_', citycode)

-- 字符串拆分, '126.616035,45.764964' -> 126.616035 和 45.764964
-- 1代表第一个，-1代表最后一个
SELECT bd_lon=SUBSTRING_INDEX(gps,',', 1), bd_lat=substring_index(gps,',', -1);
```

## SELECT

### SELECT-正则

```SQL
-- like: %代表多个任意字符, _代表单个任意字符
-- escape: 指定转义字符
select SCHEMA_NAME from information_schema.SCHEMATA WHERE SCHEMA_NAME like "netbar/_%" escape '/'
-- REGEXP: 正则匹配
select SCHEMA_NAME from information_schema.SCHEMATA WHERE SCHEMA_NAME REGEXP "^netbar_[0-9]"
SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME REGEXP "^netbar_[0-9]{10}$";
```

### SELECT-CASE

```SQL
SELECT k1,
  CASE
    WHEN k2 > 150 THEN '>150'
    WHEN k2 > 120 THEN '120< k2 >150'
    ELSE '<120'
  END as v
FROM t1
```

## INSERT/REPLACE

```SQL
-- 表复制
INSERT INTO t1 SELECT * FROM t2;
-- 表复制：指定字段
INSERT INTO t1 (k1, k2)
SELECT k1, k2 FROM t2

-- REPLACE INTO: 用法与Insert相同
-- 当KEY不存在时，等价于Delete
-- 当KEY存在时，先Delete然后Insert，未设定的字段按照默认值处理

-- INSERT INTO ** ON DUPLICATE KEY UPDATE
-- 当KEY存在时，只更新指定字段
INSERT INTO t1 (k1, k2)
SELECT k1, k2 FROM t2
ON DUPLICATE KEY UPDATE t1.k1=t2.k1
```

## Update

```SQL
-- 联表更新：方式1
UPDATE t1 as a
SET a.test_key=(SELECT test_key FROM t2 as b WHERE a.id=b.id);
-- 联表更新：方式2
UPDATE t1 as a
LEFT JOIN t2 as b ON a.id=b.id
SET a.test_key=b.test_key
-- 联表更新： 方式3
UPDATE t1 as a, t2 as b
SET a.test_key=b.test_key
WHERE a.id=b.id
```

## 表

```sql
-- 创建库
CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
-- 数据库遍历
SELECT SCHEMA_NAME FROM information_schema.SCHEMATA
-- 创建表
CREATE TABLE IF NOT EXISTS olcustomer(
    icafe bigint NOT NULL COMMENT '网吧号',
    uid varchar(10) NOT NULL COMMENT '用户ID',
    grade int NOT NULL default 0 COMMENT '等级',
    uptm datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    primary key(icafe,uid)
)COMMENT='刷卡人员列表';
-- 删除
DROP TABLE IF EXISTS tn;
-- 快速清空表
TRUNCATE TABLE tn;

-- 遍历所有数据库
SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME LIKE "netbar_%";
-- 遍历指定数据库下的表
SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME LIKE 'bar_%' AND TABLE_SCHEMA='netbaropt';
-- 检查索引
SELECT INDEX_NAME FROM information_schema.statistics WHERE table_schema=@db AND table_name = 'duty' AND index_name = 'idx_tmbegin';
-- 创建时间
SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_TIME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA LIKE 'netbar_2%' AND TABLE_NAME='duty';
```

### 列操作

```sql
-- 列遍历
SELECT COLUMN_NAME FROM information_schema.`COLUMNS` WHERE TABLE_SCHEMA='库名' AND TABLE_NAME='表名';
-- 添加列
ALTER TABLE user ADD age int(3);
-- 删除列
ALTER TABLE user DROP COLUMN age;
-- 修改列
ALTER TABLE `user` MODIFY COLUMN age tinyint;
-- 添加主键
ALTER TABLE user ADD PRIMARY KEY (id);
-- 删除主键
ALTER TABLE user DROP PRIMARY KEY;
-- 添加索引
ALTER TABLE 表名 ADD INDEX 索引名 (列名) ;
-- 删除索引
DROP INDEX index_name ON table_name;
```

### 内存表

```sql
CREATE TABLE t3 (i INT) ENGINE = MEMORY;
```

### 视图

```sql
-- 删除
DROP VIEW IF EXISTS v_olcustomer;
```

## 时间

```SQL
SET @d1='2019-10-20';
SET @d2='2019-10-27';
SET @dc=TIMESTAMPDIFF(DAY, @d1, @d2);   -- 时间差：日

SELECT tkey, count(1) / @dc FROM t
WHERE uptime BETWEEN @d1 AND @d2
GROUP BY tkey

-- 时间差
set @dt = NOW();

select Date_Add(@dt, interval 1 day); -- add 1 day
select Date_Add(@dt, interval 1 hour); -- add 1 hour
select Date_Add(@dt, interval 1 minute); -- ...
select Date_Add(@dt, interval 1 second);
select Date_Add(@dt, interval 1 microsecond);
select Date_Add(@dt, interval 1 week);
select Date_Add(@dt, interval 1 month);
select Date_Add(@dt, interval 1 quarter);
select Date_Add(@dt, interval 1 year);

select Date_Add(@dt, interval -1 day); -- sub 1 day
-- 时间差
SELECT TIMESTAMPDIFF(DAY,'2012-10-01','2013-01-13');
SELECT TIMESTAMPDIFF(MONTH,'2012-10-01','2013-01-13');
```

```SQL
-- 时间 -> 字符串
SET @DB := CONCAT('database.database_', DATE_FORMAT(NOW(), '%Y%m%d'));
SET @LIST := CONCAT('netbaropt.list_', DATE_FORMAT(NOW(), '%Y%m%d'));
-- 字符串 -> 时间
select str_to_date('2008-08-09 08:09:30', '%Y-%m-%d %h:%i:%s');

-- 时间戳
select unix_timestamp('2008-08-08 12:30:00');    -- 1218169800
select from_unixtime(1218169800);                -- 2008-08-08 12:30:00
select from_unixtime(1218169800, '%Y-%m-%d %h:%i:%s');    -- 2008-08-08 12:30:00

-- 其他常用函数
AddDate()     --增加一个日期（天、周等）
AddTime()     --增加一个时间（时、分等）
DateDiff()    --计算两个日期之差（日）
Date_Add()    --高度灵活的日期运算函数
Date_Format() --返回一个格式化的日期或时间串

CurDate() --返回当前日期
CurTime() --返回当前时间

Year()    --返回一个日期的年份部分
Month()   --返回一个日期的月份部分
Day()     --返回一个日期的天数部分
Hour()    --返回一个时间的小时部分
Minute()  --返回一个时间的分钟部分
Second()  --返回一个时间的秒部分

Date()        --返回日期时间的日期部分
Time()        --返回一个日期时间的时间部分
DayOfWeek()   --对于一个日期，返回对应的星期几
```

## 常用函数

```sql
AVG()   --返回某列的平均值
COUNT() --返回某列的行数
MAX()   --返回某列的最大值
MIN()   --返回某列的最小值
SUM()   --返回某列值之和

SIN()   --正弦
COS()   --余弦
TAN()   --正切
ABS()   --绝对值
SQRT()  --平方根
MOD()   --余数
EXP()   --指数
PI()    --圆周率
RAND()  --随机数
```
