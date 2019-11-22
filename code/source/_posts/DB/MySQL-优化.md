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

## 常规Demo

+ 表复制: `INSERT INTO t1 SELECT * FROM t2`

## 字符串

```SQL
-- REPLACE
SELECT REPLACE('aaa.mysql.com','a','w');
```

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

## INSERT/REPLACE

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

## 优化

### SELECT优化

频繁操作的库不适合开启查询缓存

```sql
-- 当你查询表的有些时候，你已经知道结果只会有一条结果，但因为你可能需要去fetch游标，或是你也许会去检查返回的记录数。
-- 在这种情况下，加上 LIMIT 1 可以增加性能。这样一样，MySQL数据库引擎会在找到一条数据后停止搜索，而不是继续往后查少下一条符合记录的数据。
SELECT * FROM tn where id = 1 LIMIT 1
```

### 表优化

+ VARCHAR -> ENUM
  + ENUM 类型是非常快和紧凑的。在实际上，其保存的是 TINYINT，但其外表上显示为字符串。
  + 这样一来，用这个字段来做一些选项列表变得相当的完美; 比如“性别”，“国家”，“民族”，“状态”或“部门”，字段的取值是有限而且固定的

#### 查询缓存检查是否开启

```sql
show variables like '%cache%';
-- query_cache_size
-- query_cache_type = 0/1
show variables like '%qcache%';        -- 命中情况
-- Qcache_hits

-- 0: 关闭, 1: 开启
-- 临时关闭
set global query_cache_size=0
set global query_cache_type=0
-- 永久关闭: 修改配置文件my.cnf
query_cache_type=0
query_cache_size=0

-- 语句指定
select sql_no_cache count(*) from users;    -- 无缓存
select sql_cache count(*) from users;       -- 缓存

-- 单条大数据
-- 默认1M, 改为10M
show variables like 'max_allowed_packet';
set global max_allowed_packet = 10*1024*1024

-- 特定函数导致不缓存
-- 某些查询语句会让MySQL不使用缓存。请看下面的示例：
-- 查询缓存不开启
$r = mysql_query("SELECT username FROM user WHERE signup_date >= CURDATE()");
-- 开启查询缓存
$today = date("Y-m-d");
$r = mysql_query("SELECT username FROM user WHERE signup_date >= '$today'");
-- 上面两条SQL语句的差别就是 CURDATE() ，MySQL的查询缓存对这个函数不起作用。
-- 所以，像 NOW() 和 RAND() 或是其它的诸如此类的SQL函数都不会开启查询缓存，因为这些函数的返回是会不定的易变的。
-- 所以，你所需要的就是用一个变量来代替MySQL的函数，从而开启缓存。

-- 无缓冲查询
-- 并不像mysql_query()一样去自动fethch和缓存结果。这会相当节约很多可观的内存，尤其是那些会产生大量结果的查询语句
-- 你不需要等到所有的结果都返回，只需要第一行数据返回的时候，你就可以开始马上开始工作于查询结果了。
mysql_unbuffered_query()
-- 限制：你要么把所有行都读走，或是你要在进行下一次的查询前调用mysql_free_result() 清除结果
-- 而且， mysql_num_rows() 或 mysql_data_seek() 将无法使用。
```

### 索引优化

```sql
EXPLAIN SELECT COUNT(*) FROM shengyibao.icafe_services WHERE id="1";
```

| 项 | 值 | 描述 | 备注 |
| -- | -- | -- | -- |
| id | | 如果多条的话, 代表该语句分多次运行, id顺序代表执行顺序
| select_type | simple | 表示简单查询 | 查询类型
| | primary | 最外层的 select 查询
| | DEPENDENT SUBQUERY | 子查询中的第一个 select 查询,依赖于外部 查询的结果集
| | DERIVED | 用于 from 子句里有子查询的情况。 MySQL 会 递归执行这些子查询, 把结果放在临时表里。
| | UNCACHEABLE SUBQUERY | 结果集不能被缓存的子查询,必须重新为外 层查询的每一行进行评估。
| | UNCACHEABLE UNION | UNION 中的第二个或随后的 select 查询,属 于不可缓存的子查询
| type | system | 表仅有一行, const的特例
| | const | const 用于用常数值比较 PRIMARY KEY 时。当 查询的表仅有一行时,使用 System。
| | eq_ref | 关联表 - 最多匹配一行, 除const外最优
| | ref | 关联表 - 所有内容都是索引关联
| | ref_or_null |  等同于ref+NULL判断
| | ref_or_null | 等同于ref+NULL判断
| | index_merge | 索引合并优化方法 - 查询中使用多个索引
| | key | 列包含了使用的索引的清单
| | unique_subquery | 子查询, 不建议使用
| | index_subquery | 子查询, 使用非唯一性索引
| | range | 范围查询
| | index | 索引全表扫描
| | all | 行全表扫描
| possible_keys | | 指出 MySQL 能在该表中使用哪些索引有助于 查询。如果为空,说明没有可用的索引。
| key | | MySQL 实际从 possible_key 选择使用的索引。 如果为 NULL,则没有使用索引。
| key_length | | 使用的索引长度, 越小也好
| ref | | 显示索引的哪一列被使用了
| rows | | 检查行数, 越小越好
| Extra | Using Index | 使用索引 | 解决查询的详细信息
| | using filesort | 外部排序
| | Using temporary | 使用到临时表

### 配置优化

+ table_open_cache
  + 该值比较大时, 占用内存较多
  + 建议值: max_connections * 表数目, 一段时间内可能打开的表对象总和
  + 释放规则:
    + 当缓冲已满，而连接想要打开一个不在缓冲中的表时。
    + 当缓冲数目已经超过了table_open_cache设置的值，mysql开始使用LRU算法释放表对象。
    + 当你用flush tables;语句时。

```sql
SHOW GLOBAL STATUS LIKE 'Open%tables'
-- Open_tables: 当前打开的table对象数量
-- Opened_tables: 打开过的表的数量总和

-- MYSQL运行时长
show global status like 'uptime';
-- Opened_tables/Uptime的值过大说明table_open_cache过小，
  -- 导致一些table对象（即下文说的table对象）经常会刷出server层，需要的时候再创建，最终导致此计数过大。

-- 当前打开的表
show open tables;
```

### 碎片整理

```sql
-- 在OPTIMIZE TABLE运行过程中，MySQL会锁定表
-- delete 操作不能够直接回收被删除数据占用的数据文件空间
OPTIMIZE [LOCAL | NO_WRITE_TO_BINLOG] TABLE tbl_name [, tbl_name] ...
ALTER TABLE 表名 ENGINE = Innodb;		-- 空alter语句，但是也会达到优化的效果，它会重建整个表
-- 表数据状态
show table status;
show table STATUS like '表名';
-- 分析表
ANALYZE TABLE 表名;    -- 分析表, 关键字分布等，确保show查询的表状态是正确的
-- 备记
-- 优化表+重组数据，并不会完全释放剩余空间(Data_free)，根据表当前数据量可能会保留一部分(通常是默认值1-4M，压缩表2M，非压缩表4M)
```

## 状态检查

### 内存占用

```sql
FLUSH TABLES;
FLUSH STATUS;

-- 清理: FLUSH, 缓慢释放已占用内存
FLUSH flush_option [,flush_option]
-- HOSTS: 清空主机缓存表
-- LOGS:  关闭当前的二进制日志文件并创建一个新文件
-- TABLES: 关闭所有打开的表，同时该操作将会清空查询缓存中的内容。
        -- FLUSH TABLES WITH READ LOCK  关闭所有打开的表，同时对于所有数据库中的表都加一个读锁
        -- 直到显示地执行unlock tables，该操作常常用于数据备份的时候。
-- STATUS: 重置大多数状态变量到0。
-- QUERY CACHE: 重整查询缓存，消除其中的碎片，提高性能，但是并不影响查询缓存中现有的数据，
             -- 这点和Flush table 和Reset Query  Cache（将会清空查询缓存的内容）不一样的。

-- 各种内存空间配置项
show variables where variable_name in (
'innodb_buffer_pool_size','innodb_log_buffer_size','innodb_additional_mem_pool_size','key_buffer_size','query_cache_size'
);
show variables where variable_name in (
'read_buffer_size','read_rnd_buffer_size','sort_buffer_size','join_buffer_size','binlog_cache_size','tmp_table_size'
);

used_Mem = key_buffer_size + query_cache_size + innodb_buffer_pool_size
used_Mem += innodb_log_buffer_size
used_Mem += 210 * (
    read_buffer_size
    + read_rnd_buffer_size
    + sort_buffer_size
    + join_buffer_size
    + binlog_cache_size
    + tmp_table_size
    + thread_stack
    + thread_cache_size
    + net_buffer_length
    + bulk_insert_buffer_size
)
```

### 未提交事务

```sql
select t.trx_mysql_thread_id from information_schema.innodb_trx t;
-- kill 3836183;

-- 查询 正在执行的事务：
SELECT * FROM information_schema.INNODB_TRX;

-- 查看正在锁的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS; 

-- 查看等待锁的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS;

-- 长时间未结束的查询
-- COMMAND='Query' AND INFO IS NOT NULL
select * from information_schema.`PROCESSLIST` where id <> CONNECTION_ID() ORDER BY time desc;
-- 长时间执行的查询(1小时), 可以直接kill掉返回的id
select * from information_schema.processlist
where time >= 3600 and command not in ('sleep')
    and user not in ('system user', 'replicator', 'aurora', 'event_scheduler')
    and state not like ('waiting for table%lock');
```

### 锁等待

```sql
SELECT l.* FROM
  (
    SELECT 'Blocker' role, p.id, p.USER,
      LEFT ( p.HOST, locate(':', p.HOST) - 1 ) HOST,
      tx.trx_id, tx.trx_state, tx.trx_started,
      timestampdiff( SECOND, tx.trx_started, now() ) duration,
      lo.lock_mode, lo.lock_type, lo.lock_table, lo.lock_index, tx.trx_query, lw.requesting_trx_id Blockee_trx
    FROM
      information_schema.innodb_trx tx,
      information_schema.innodb_lock_waits lw,
      information_schema.innodb_locks lo,
      information_schema. PROCESSLIST p
    WHERE
      lw.blocking_trx_id = tx.trx_id AND p.id = tx.trx_mysql_thread_id AND lo.lock_id = lw.blocking_lock_id
    UNION
      SELECT
        'Blockee' role, p.id, p.USER, LEFT ( p.HOST, locate(':', p.HOST) - 1 ) HOST,
        tx.trx_id, tx.trx_state, tx.trx_started,
        timestampdiff( SECOND, tx.trx_started, now() ) duration,
        lo.lock_mode, lo.lock_type, lo.lock_table, lo.lock_index, tx.trx_query, NULL
      FROM
        information_schema.innodb_trx tx,
        information_schema.innodb_lock_waits lw,
        information_schema.innodb_locks lo,
        information_schema. PROCESSLIST p
      WHERE
        lw.requesting_trx_id = tx.trx_id AND p.id = tx.trx_mysql_thread_id AND lo.lock_id = lw.requested_lock_id
  ) l
ORDER BY
  role DESC,
  trx_state DESC;
```

### 日志

```sql
show master logs;
show binary logs;
-- 远程提取: 下载后可直接cat查看
mysqlbinlog  -u** -p -h***.mysql.rds.aliyuncs.com --read-from-remote-server mysql-bin.000497 >a.sql
```
