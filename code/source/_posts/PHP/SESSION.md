---
title: Session
tags: 
  - Session
categories: 
  - PHP
description: Session, login
date: 2019-11-16 18:06:07
updated: 2019-11-16 18:06:07
---

## 登陆

```PHP
check();

function check(){
    if(substr($_SERVER['REMOTE_ADDR'], 0, 10) == '192.168.1.')
    {
        // 内网放行
        return;
    }
    if(!$_SESSION['is_login'] == '1')
    {
        // 已经登陆: 调整Session过期时间
        ini_set('session.gc_maxlifetime', "86400"); // 秒
        ini_set("session.cookie_lifetime","86400"); // 秒
        return;
    }
    // 强制跳转到login
    echo '<script>window.location.href="./login.html";</script>';
    die;
}


if ($_REQUEST['name'] == '...' && $_REQUEST['pwd'] == '***') {
    // 标记登陆
    $_SESSION['is_login'] = 1;
}
```
