---
title: 环境
tags: 
  - PHPStorm
  - phpStudy
categories: 
  - PHP
description: 环境, PHPStorm, phpStudy
date: 2019-11-20 19:20:44
updated: 2019-11-20 19:20:44
---

## 环境

+ [phpStudy](https://www.xp.cn/)

## PHPStorm

+ 注册码: [http://idea.lanyus.com/](http://idea.lanyus.com/)
  + 也可以到[PHP中文网](http://www.php.cn/)找
+ 配置
  + `Appearance`->`Theme`->选择`Darcula`，暗色调看着比较舒服
    + 字体 -> 微软雅黑，14
  + `Editor`->`font`  首先Scheme save自己的方案，然后字体改 Consolas|Courier|Source Code Pro等宽字体，16
    + `General`->`Appearance`->`Show line numbers` && `Show whitespace`
+ 其他
  + `Editor`->`Code Style`->`PHP`：空行 空格
  + `Editor`->`Inspections`->`Spelling`: 取消选中(单词检查)
  + `File Encodings`-> IDE Encoding: UTF-8;
  + `File Encodings`-> Project Encoding: UTF-8;

### 快捷键

+ 查找 / 选中
  + `Alt+左键`: 多选
  + `Ctrl+Alt+Shift+左键`: 选中多行

  + `Alt+J`: 搜索并选中
  + `CTRL+F`: 在当前窗口查找文本
  + `CTRL+SHIFT+F`: 在指定路径查找文本
  + `CTRL+R`: 当前窗口替换文本
  + `CTRL+SHIFT+R`: 在指定路径替换文本
  
  + `CTRL+SHIFT+V`: 可以复制多个文本
  + `CTRL+D`: 复制行
  + `CTRL+SHIFT+[]`: 选中块代码，可以快速复制
  
  + `CTRL+E`: 最近打开的文件

+ 结构化查找
  + `Ctrl+F12`: 文件结构
  + `alt+'7'`: 显示当前的类/函数结构
  + `Ctrl+Shift+A`: 查找快捷键
  + `CTRL+N`: 查找类
  + `CTRL+SHIFT+N`: 查找文件，打开工程中的文件(类似于eclipse中的ctrl+shift+R)，目的是打开当前工程下任意目录的文件
  + `CTRL+SHIFT+ALT+N`: 查找类中的方法或变量(JS)
  + `SHIFT+F6`  重命名,重构 当前区域内变量重命名/重构

+ 跳转 / 定位
  + `F2`: 高亮错误或警告快速定位
  + `F4`: 查找变量来源
  + `Ctrl+左键`: 跳转到定义
  + `CTRL+G`: 定位行，跳转行
  + `Ctrl+Shift+Backspace`: 键导航到最后编辑的位置
  + `CTRL+[]`: 光标移动到{}[]开头或结尾位置，python跳转到函数头
  + `CTRL+ALT+ ←/→`: 返回上次编辑的位置
  + `ALT+ ↑/↓`: 在方法间快速移动定位

+ 书签
  + `ALT+ ←/→`: 切换代码视图，标签切换
  + `F11`: 书签助记符
  + `Shift+F11`: 显示书签
  + `Ctrl+Shift+[0-9]`: 创建编号书签
  + `Ctrl+[0-9]`: 转到编号书签

+ 折叠
  + `ctrl+'-/+'`: 可以折叠代码块
  + `ctrl+'.'`: 折叠选中代码所属代码块
  + `Ctrl+Shift+小键盘+`：展开全部
  + `Ctrl+Shift+小键盘-`：关闭全部

+ 美化 / 优化
  + `CTRL+ALT+L`: 格式化代码
  + `CTRL+ALT+I`: 自动缩进
  + `CTRL+ALT+O`: 优化导入的类和包(冲突：QQ截屏识字)

+ 提示 / 快捷输入
  + `CTRL+P`: 方法参数提示，显示默认参数
  + `CTRL+ALT+T`:  把选中的代码放在 TRY{} IF{} ELSE{} 里
  + `Ctrl+Shift+U`: 选中的字符大小写转换

+ 本地历史VCS/SVN
  + `Alt+反引号`: 快速弹出VCS菜单
  + `Ctrl+K`: 提交项目VCS
  + `Ctrl+T`: 更新项目从VCS
  + `Alt+Shift+C`: 查看最近发生的变化
