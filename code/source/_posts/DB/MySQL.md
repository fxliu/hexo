---
title: MySQL
tags: 
  - SQL
categories: 
  - MySQL
description: SQL
date: 2019‎-10‎-27‎ 13:53:32
updated: 2019‎-10‎-27‎ 13:53:32
---

## 常规Demo

+ 表复制: `INSERT INTO t1 SELECT * FROM t2`

## SELECT

```SQL
-- CASE
SELECT k1,
  CASE
    WHEN k2 > 150 THEN '>150'
    WHEN k2 > 120 THEN '120< k2 >150'
    ELSE '<120'
  END as v
FROM t1
```

## Insert

```SQL
-- INSERT INTO
INSERT INTO t1 SELECT * FROM t2;
-- INSERT INTO
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

## 时间

```SQL
SET @d1='2019-10-20';
SET @d2='2019-10-27';
SET @dc=TIMESTAMPDIFF(DAY, @d1, @d2);   -- 时间差：日

SELECT tkey, count(1) / @dc FROM t
WHERE uptime BETWEEN @d1 AND @d2
GROUP BY tkey

-- 时间差
set @dt = now();

select date_add(@dt, interval 1 day); -- add 1 day
select date_add(@dt, interval 1 hour); -- add 1 hour
select date_add(@dt, interval 1 minute); -- ...
select date_add(@dt, interval 1 second);
select date_add(@dt, interval 1 microsecond);
select date_add(@dt, interval 1 week);
select date_add(@dt, interval 1 month);
select date_add(@dt, interval 1 quarter);
select date_add(@dt, interval 1 year);

select date_add(@dt, interval -1 day); -- sub 1 day
-- 时间差
SELECT TIMESTAMPDIFF(DAY,'2012-10-01','2013-01-13');
SELECT TIMESTAMPDIFF(MONTH,'2012-10-01','2013-01-13');
```

```SQL
-- 时间 -> 字符串
SET @DB := CONCAT('database.database_', DATE_FORMAT(now(), '%Y%m%d'));
SET @LIST := CONCAT('netbaropt.list_', DATE_FORMAT(now(), '%Y%m%d'));
-- 字符串 -> 时间
select str_to_date('2008-08-09 08:09:30', '%Y-%m-%d %h:%i:%s');

-- 时间戳
select unix_timestamp('2008-08-08 12:30:00');    -- 1218169800
select from_unixtime(1218169800);                -- 2008-08-08 12:30:00
select from_unixtime(1218169800, '%Y-%m-%d %h:%i:%s');    -- 2008-08-08 12:30:00
```
