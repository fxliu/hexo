---
title: MySQL-存储过程
tags: 
  - SQL
  - 存储过程
categories: 
  - MySQL
description: SQL, 存储过程
date: 2019-11-22 09:27:41
updated: 2019-11-22 09:27:41
---

## 基础

+ 不支持打印输出
+ 不支持SQL语句输出
+ 支持参数传入传出
+ 批量数据只能创建临时表, 存储过程中保存数据到临时表, 存储过程外从临时表提取输出

```sql
-- 同名存储过程存在则删除
DROP PROCEDURE IF EXISTS `proc_adder`;
-- 重置语句结束符
DELIMITER ;;
-- 创建存储过程：一个加法器
CREATE PROCEDURE proc_adder(IN a int, IN b int, OUT sum int)
BEGIN
    DECLARE c int;
    if a is null then set a = 0;
    end if;
    if b is null then set b = 0;
    end if;
    set sum = a + b;
END
;;
DELIMITER ;    -- 还原默认语句结束符
-- 调用
set @b=5;
call proc_adder(2,@b,@s);
select @s as sum;
```

### 语句返回值接收

```sql
SELECT count(*) into @c FROM shengyibao.area;
SELECT @c;
-- ----------------------------------------
SET @STMT = CONCAT("SELECT count(*) into @c FROM shengyibao.area;");
PREPARE STMT FROM @STMT;
EXECUTE STMT;
SELECT @c;
```

### 重建索引

```sql
-- SQL不支持直接使用IF语句，所以只能使用负载均衡
DROP PROCEDURE IF EXISTS test;
DELIMITER ;;
CREATE PROCEDURE test (OUT pv TEXT) DETERMINISTIC
BEGIN
  IF NOT EXISTS(SELECT INDEX_NAME FROM information_schema.statistics WHERE table_schema='table_name' AND table_name = 'index_name' AND index_name = 'idx_test') THEN
    ALTER TABLE netbar_2308052252.`duty` ADD INDEX `idx_tmbegin` (`tmbegin`);
  END IF;
END;;
DELIMITER ;
-- 调用
call test(@pv);
select @pv;
```

## 案例

### 修改列

```sql
/* 遍历库，对库中指定表进行操作 */
-- 同名存储过程存在则删除
DROP PROCEDURE IF EXISTS test;
-- 置存储过程标记符号";;"
DELIMITER ;;
-- 创建存储过程"test"
CREATE PROCEDURE test (OUT pv TEXT) DETERMINISTIC
BEGIN
  DECLARE time_b VARCHAR(64) DEFAULT '2018-04-14 8:00:00';  -- 自定义变量

  DECLARE done tinyint default 0;   -- 游标结束判定符
  DECLARE db VARCHAR(64);           -- 游标数据接收变量
  -- 创建游标
  DECLARE cur CURSOR FOR
    SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME REGEXP "^testdb_[0-9]{10}$";
  -- 设定游标结束标记
  DECLARE continue handler for sqlstate '02000' SET done=1;
  -- 打开游标
  OPEN cur;
  -- 提取游标值
  FETCH cur INTO db;
  -- 循环检查游标
  WHILE done<>1 DO
    SET @db = db;
    -- ---------------------------------------------------------------------------------------------
    -- 不需要IF，如果列未发生变化，语句会很快结束
    -- AFTER用于指定调整列位置
    SET @STMT = CONCAT('
      ALTER TABLE ', @db, '.`member`
      MODIFY COLUMN `col_name1`  datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT \'创建时间\' AFTER `col_name2`;');
    PREPARE STMT FROM @STMT;
    EXECUTE STMT;
    -- -----------------------------------------------------------------------------------------------
    -- 下一个游标
    FETCH cur INTO db;
  END WHILE;
  -- 关闭游标
  CLOSE cur;
END;;   -- 存储过程结束标记
DELIMITER ; -- 重置存储过程结束标记为默认值

-- 调用该存储过程，注意：输出参数必须是一个带@符号的变量，支持多参数传入传出
CALL test (@pv);

-- 显示
SELECT @pv;
```

### 添加列

```sql
DROP PROCEDURE IF EXISTS test;

DELIMITER ;;
CREATE PROCEDURE test (OUT pv TEXT) DETERMINISTIC
BEGIN
  SET pv = '0';
  -- 检查列是否存在
  IF NOT EXISTS(SELECT * FROM information_schema.`COLUMNS` WHERE TABLE_SCHEMA='NetbarOpt' AND TABLE_NAME='table_name' AND COLUMN_NAME='col_name')
  THEN
    -- 不存在则创建
    SET @bar_tn = 'table_name';
    SET @STMT = CONCAT("ALTER TABLE `", @bar_tn,"` ADD COLUMN `col_name` VARCHAR (50) NULL AFTER `opt_time`;");
    PREPARE STMT FROM @STMT;
    EXECUTE STMT;
    SET pv = @STMT;
  END IF;
END;;
DELIMITER ;

/* 调用该存储过程，注意：输出参数必须是一个带@符号的变量 */
CALL test (@pv);
SELECT @pv;
```
