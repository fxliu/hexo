---
title: exec
tags: 
  - exec
categories: 
  - PHP
description: exec
date: 2023-06-05 09:58:29
updated: 2023-06-05 09:58:29
---

## exec

```php
// exec ( string $command [, array &$output [, int &$return_var ]] )；
// $output 是一个数组, 每行一个元素
// return_var 是程序退出返回值
exec($cmd, $output, $resultCode);
```

## proc_open

```php
$descriptorspec = array(
    0 => array("pipe", "r"),    //标准输入，子进程从此管道读取数据
    1 => array("pipe", "w"),    //标准输出，子进程向此管道写入数据
    2 => array("file", dirname(__FILE__) . "\\error-output.txt", "a")    //标准错误，写入到指定文件
);

$process = proc_open('cmd', $descriptorspec, $pipes);
if (is_resource($process)) {
    fwrite($pipes[0], "dir\n");
    fclose($pipes[0]);

    echo stream_get_contents($pipes[1]);
    fclose($pipes[1]);

    proc_close($process);
}
```
