---
title: Git
tags: 
  - Git
  - Github
categories: 
  - Tools
description: Git, Github
date: 2019-09-28 11:04:52
updated: 2019-09-28 11:04:52
---

## 常规指令

+ 恢复误删除文件(尚未提交到本地库情况)：`git checkout -- file`
  + `git status` 查看删除文件，中文会转码，但git checkout时，直接用中文使用转码文件名不好使
  + 恢复所有
    + `git reset head ./`
    + `git checkout ./`
+ 恢复误删除文件(已提交到本地库/远程库情况)
  + `git reset --hard + 版本号`版本回溯, 再`git checkout -- file`

## gihub

[git-简明指南](http://rogerdudler.github.io/git-guide/index.zh.html)
[猴子都能懂得GIT入门](https://backlog.com/git-tutorial/cn/)

### fork

分支别人的仓库到自己仓库

+ 打开大佬的github，点击右上角的fork按钮
+ 然后回到自己的github->Repositories，同名的仓库已经存在了，就是这么简单
